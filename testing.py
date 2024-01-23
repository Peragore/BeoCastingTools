import ReplayHandler as rh
import json
with open('json/upgrades.json', 'r') as f:
    upgrade_dict = json.load(f)
f.close()

packet = rh.generate_plot_data(upgrade_dict)

with open('json/datastream.json', 'w') as f:
    json.dump(packet, f)
f.close()