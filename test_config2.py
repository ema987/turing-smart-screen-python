import sys
import yaml

def load_yaml(file_path):
    with open(file_path, "r", encoding="utf8") as f:
        return yaml.safe_load(f)

def copy_default(default, theme):
    for k, v in default.items():
        if k not in theme:
            theme[k] = v
        if type(v) == type({}):
            copy_default(default[k], theme[k])

THEME_DEFAULT = load_yaml("res/themes/default.yaml")
THEME_DATA = load_yaml("res/themes/Overdrive5080/theme.yaml")

copy_default(THEME_DEFAULT, THEME_DATA)

gpu = THEME_DATA['STATS']['GPU']
print(f"PERCENTAGE.TEXT.SHOW: {gpu['PERCENTAGE'].get('TEXT', {}).get('SHOW')}")
print(f"TEMPERATURE.TEXT.SHOW: {gpu['TEMPERATURE'].get('TEXT', {}).get('SHOW')}")
print(f"MEMORY_PERCENT.TEXT.SHOW: {gpu['MEMORY_PERCENT'].get('TEXT', {}).get('SHOW')}")
print(f"VIRTUAL.USED.SHOW: {THEME_DATA['STATS']['MEMORY']['VIRTUAL'].get('USED', {}).get('SHOW')}")

