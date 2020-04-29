
import appdaemon.plugins.hass.hassapi as hass

class MotionLight(hass.Hass):

  def initialize(self):
    self.globals = self.get_app('globals')
    self.sensor = self.args['sensor']
    self.light = self.args['light']
    self.debug = self.args['debug']

    #listeners
    self.listen_state(self.lights_on, self.sensor, new='on')
    if self.light == 'light.front_door':
      self.listen_state(self.lights_off, self.sensor, new='off')

    self.log('Successfully initialized ' + self.light + ' motion app!' , level='INFO')


  def lights_on(self, entity, attribute, old, new, kwargs):
    fan = self.get_state('input_boolean.in_bed')
    status = self.get_state(self.light)
    home = self.get_state('input_boolean.home')
    living_room_motion = self.get_state('input_boolean.living_room_motion')
    if home == 'on':
      if status == 'off':
        if self.light == 'light.living_room' and living_room_motion == 'off':
          self.globals.debug('Living Room not turned on due to override', self.debug)
          return
        if fan == 'on':
          if self.light == 'light.bedroom':
            self.globals.debug('Bedroom motion detected, but fan on so lights stay off', self.debug)
            return
          else:
            self.turn_on(self.light, rgb_color=self.globals.nightlightRGB, brightness=self.globals.nightlightBrightness, transition=1)
            self.globals.debug('Turned on ' + self.light + ' dim because fas was on and motion was detected', self.debug)
        else:
          self.turn_on(self.light)
          self.globals.debug('Turned on ' + self.light + ' because motion was detected', self.debug)
      else:
        self.globals.debug('Motion detected but light is already on', self.debug)
    else:
      self.log('Detected motion but noone is home')

  def lights_off(self, entity, attribute, old, new, kwargs):
    self.turn_off(self.light)
    self.globals.debug('Turned off ' + self.light, self.debug)

