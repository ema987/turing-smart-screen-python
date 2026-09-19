import sys
import logging
from unittest.mock import MagicMock

logging.basicConfig(level=logging.DEBUG)

import library.config as config
config.CONFIG_DATA = config.load_yaml("config.yaml")

from pathlib import Path
theme_path = Path("res/themes/" + config.CONFIG_DATA['config']['THEME'])
config.THEME_DATA = config.load_yaml(config.MAIN_DIRECTORY / theme_path / "theme.yaml")
config.THEME_DATA['PATH'] = str(config.MAIN_DIRECTORY / theme_path) + "/"
config.copy_default(config.THEME_DEFAULT, config.THEME_DATA)

import library.sensors.sensors_python as sensors
from library.stats import SystemStats, Gpu, Memory

print("--- INIT ---")
SystemStats.init(config)

Gpu.last_values_gpu_percentage = []
Gpu.last_values_gpu_mem_percentage = []
Gpu.last_values_gpu_temperature = []
Gpu.last_values_gpu_fps = []
Gpu.last_values_gpu_fan_speed = []
Gpu.last_values_gpu_frequency = []
Memory.last_values_mem_percentage = []
Memory.last_values_swap_percentage = []

from library.display import display
display.lcd = MagicMock()
display.lcd.DisplayText = MagicMock()
display.lcd.DisplayRadialProgressBar = MagicMock()
display.lcd.DisplayLineGraph = MagicMock()
display.lcd.DisplayProgressBar = MagicMock()

print("--- GPU ---")
Gpu.stats()

for call in display.lcd.DisplayText.mock_calls:
    kwargs = call[2]
    print(f"GPU DisplayText: text='{kwargs.get('text')}' X={kwargs.get('x')} Y={kwargs.get('y')} Color={kwargs.get('font_color')} BG={kwargs.get('background_image')}")

print("\n--- MEMORY ---")
display.lcd.DisplayText.reset_mock()
Memory.stats()

for call in display.lcd.DisplayText.mock_calls:
    kwargs = call[2]
    print(f"MEM DisplayText: text='{kwargs.get('text')}' X={kwargs.get('x')} Y={kwargs.get('y')} Color={kwargs.get('font_color')} BG={kwargs.get('background_image')}")
