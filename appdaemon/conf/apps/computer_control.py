import appdaemon.plugins.hass.hassapi as hass
import my_secrets
import requests


class ComputerControl(hass.Hass):

  def initialize(self):
    self.globals = self.get_app('globals')

    self.log('Successfully initialized computer control!' , level='INFO')

  def computer_on(self):
    self.call_service('wake_on_lan/send_magic_packet', mac=my_secrets.LivingRoom_MAC, broadcast_address=my_secrets.LivingRoom_IP)
    self.log('turned computer on', level='INFO')

  def computer_off(self):
    r = requests.get("http://" + my_secrets.LivingRoom_IP  + my_secrets.LivingRoom_Hibernate)
    self.log('turned computer off', level='INFO')

