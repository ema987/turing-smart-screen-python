import sys
import logging
from pathlib import Path
from unittest.mock import MagicMock

logging.basicConfig(level=logging.DEBUG)

import library.config as config
config.CONFIG_DATA = config.load_yaml("config.yaml")

theme_path = Path("res/themes/" + config.CONFIG_DATA['config']['THEME'])
config.THEME_DATA = config.load_yaml(config.MAIN_DIRECTORY / theme_path / "theme.yaml")
config.THEME_DATA['PATH'] = str(config.MAIN_DIRECTORY / theme_path) + "/"
config.copy_default(config.THEME_DEFAULT, config.THEME_DATA)

from library.display import display
display.lcd = MagicMock()
display.lcd.DisplayText = MagicMock()
display.lcd.DisplayRadialProgressBar = MagicMock()
display.lcd.DisplayLineGraph = MagicMock()
display.lcd.DisplayProgressBar = MagicMock()

import library.sensors.sensors_python as sensors
# Mock GPU stats
sensors.Gpu.is_available = MagicMock(return_value=True)
sensors.Gpu.stats = MagicMock(return_value=(0.10, 0.20, 1000.0, 8000.0, 50.0))
sensors.Gpu.fps = MagicMock(return_value=60)
sensors.Gpu.fan_percent = MagicMock(return_value=45)
sensors.Gpu.frequency = MagicMock(return_value=1500.0)

from library.stats import Gpu
Gpu.init(config)
Gpu.stats()

print("\n--- DisplayText Calls ---")
for call in display.lcd.DisplayText.mock_calls:
    args, kwargs = call[1], call[2]
    print(f"text='{kwargs.get('text')}' X={kwargs.get('x')} Y={kwargs.get('y')}")

print("\n--- DisplayRadialProgressBar Calls ---")
for call in display.lcd.DisplayRadialProgressBar.mock_calls:
    args, kwargs = call[1], call[2]
    print(f"value={kwargs.get('value')} X={kwargs.get('xc')} Y={kwargs.get('yc')}")

