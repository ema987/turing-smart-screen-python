import yaml
with open("res/themes/Overdrive5080/theme.yaml", "r") as f:
    theme = yaml.safe_load(f)

# Let's inspect what is currently overlapping
print("GPU PERCENT RADIAL X:", theme['STATS']['GPU']['PERCENTAGE']['RADIAL']['X'])
print("MEMORY PERCENT RADIAL X:", theme['STATS']['GPU'].get('MEMORY_PERCENT', {}).get('RADIAL', {}).get('X'))
print("TEMPERATURE GRAPH X:", theme['STATS']['GPU']['TEMPERATURE']['LINE_GRAPH']['X'])

