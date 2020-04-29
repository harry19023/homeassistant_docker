import json
import yaml
import os
import stat
import shutil

# copy contents stat-info, mode, timestamps
shutil.copy2('.storage/core.entity_registry', '.storage/core.entity_registry_backup')
# copy owner and group
st = os.stat('.storage/core.entity_registry')
os.chown('.storage/core.entity_registry_backup', st[stat.ST_UID], st[stat.ST_GID])


with open('.storage/core.entity_registry') as f:
    data = json.load(f)

with open('rename_entities.yaml') as f:
    new_names = yaml.safe_load(f)

entities = data['data']['entities']
for entity in entities:
    if entity['entity_id'] in new_names:
        entity['name'] = new_names[entity['entity_id']]['name']
        entity['entity_id'] = new_names[entity['entity_id']]['entity_id']

with open('.storage/core.entity_registry', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)







