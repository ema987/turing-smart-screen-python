# SPDX-License-Identifier: GPL-3.0-or-later
#
# turing-smart-screen-python - a Python system monitor and library for USB-C displays like Turing Smart Screen or XuanFang
# https://github.com/mathoudebine/turing-smart-screen-python/
#
# Copyright (C) 2021 Matthieu Houdebine (mathoudebine)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This file allows to add custom data source as sensors and display them in System Monitor themes
# There is no limitation on how much custom data source classes can be added to this file
# See CustomDataExample theme for the theme implementation part

import math
import platform
from abc import ABC, abstractmethod
from typing import List


# Custom data classes must be implemented in this file, inherit the CustomDataSource and implement its 2 methods
class CustomDataSource(ABC):
    @abstractmethod
    def as_numeric(self) -> float:
        # Numeric value will be used for graph and radial progress bars
        # If there is no numeric value, keep this function empty
        pass

    @abstractmethod
    def as_string(self) -> str:
        # Text value will be used for text display and radial progress bar inner text
        # Numeric value can be formatted here to be displayed as expected
        # It is also possible to return a text unrelated to the numeric value
        # If this function is empty, the numeric value will be used as string without formatting
        pass

    @abstractmethod
    def last_values(self) -> List[float]:
        # List of last numeric values will be used for plot graph
        # If you do not want to draw a line graph or if your custom data has no numeric values, keep this function empty
        pass


# Example for a custom data class that has numeric and text values
class ExampleCustomNumericData(CustomDataSource):
    # This list is used to store the last 10 values to display a line graph
    last_val = [math.nan] * 10  # By default, it is filed with math.nan values to indicate there is no data stored

    def as_numeric(self) -> float:
        # Numeric value will be used for graph and radial progress bars
        # Here a Python function from another module can be called to get data
        # Example: self.value = my_module.get_rgb_led_brightness() / audio.system_volume() ...
        self.value = 75.845

        # Store the value to the history list that will be used for line graph
        self.last_val.append(self.value)
        # Also remove the oldest value from history list
        self.last_val.pop(0)

        return self.value

    def as_string(self) -> str:
        # Text value will be used for text display and radial progress bar inner text.
        # Numeric value can be formatted here to be displayed as expected
        # It is also possible to return a text unrelated to the numeric value
        # If this function is empty, the numeric value will be used as string without formatting
        # Example here: format numeric value: add unit as a suffix, and keep 1 digit decimal precision
        return f'{self.value:>5.1f}%'
        # Important note! If your numeric value can vary in size, be sure to display it with a default size.
        # E.g. if your value can range from 0 to 9999, you need to display it with at least 4 characters every time.
        # --> return f'{self.as_numeric():>4}%'
        # Otherwise, part of the previous value can stay displayed ("ghosting") after a refresh

    def last_values(self) -> List[float]:
        # List of last numeric values will be used for plot graph
        return self.last_val


# Example for a custom data class that only has text values
class ExampleCustomTextOnlyData(CustomDataSource):
    def as_numeric(self) -> float:
        # If there is no numeric value, keep this function empty
        pass

    def as_string(self) -> str:
        # If a custom data class only has text values, it won't be possible to display graph or radial bars
        return "Python: " + platform.python_version()

    def last_values(self) -> List[float]:
        # If a custom data class only has text values, it won't be possible to display line graph
        pass

import subprocess
import json
import time

_sensors_cache = {}
_sensors_cache_time = 0

def _get_sensors_data():
    global _sensors_cache, _sensors_cache_time
    # Cache for 1 second to avoid spawning too many processes
    if time.time() - _sensors_cache_time > 1:
        try:
            output = subprocess.check_output(['sensors', '-j'], text=True)
            _sensors_cache = json.loads(output)
            _sensors_cache_time = time.time()
        except Exception:
            _sensors_cache = {}
    return _sensors_cache

def _create_sensor_class(name, fetch_func, format_str="{:>.0f}"):
    class DynamicSensor(CustomDataSource):
        last_val = [math.nan] * 10
        def as_numeric(self) -> float:
            try:
                self.value = fetch_func(_get_sensors_data())
            except:
                self.value = math.nan
            self.last_val.append(self.value)
            self.last_val.pop(0)
            return self.value
        def as_string(self) -> str:
            if math.isnan(self.value):
                return "N/A"
            return format_str.format(self.value)
        def last_values(self) -> List[float]:
            return self.last_val
    DynamicSensor.__name__ = name
    return DynamicSensor

def _fetch_gpu_load(d):
    with open("/sys/class/drm/card1/device/gpu_busy_percent", "r") as f:
        return float(f.read().strip())

GpuLoadData = _create_sensor_class("GpuLoadData", _fetch_gpu_load, "{:>.0f}%")
GpuTempData = _create_sensor_class("GpuTempData", lambda d: d["amdgpu-pci-7900"]["edge"]["temp1_input"], "{:>.0f}°C")

FanCpuData = _create_sensor_class("FanCpuData", lambda d: d["nct6687-isa-0a20"]["CPU Fan"]["fan1_input"], "{:>.0f} RPM")
FanPumpData = _create_sensor_class("FanPumpData", lambda d: d["nct6687-isa-0a20"]["Pump Fan"]["fan2_input"], "{:>.0f} RPM")
FanSys1Data = _create_sensor_class("FanSys1Data", lambda d: d["nct6687-isa-0a20"]["System Fan #1"]["fan3_input"], "{:>.0f} RPM")
FanSys2Data = _create_sensor_class("FanSys2Data", lambda d: d["nct6687-isa-0a20"]["System Fan #2"]["fan4_input"], "{:>.0f} RPM")
FanSys3Data = _create_sensor_class("FanSys3Data", lambda d: d["nct6687-isa-0a20"]["System Fan #3"]["fan5_input"], "{:>.0f} RPM")
FanSys6Data = _create_sensor_class("FanSys6Data", lambda d: d["nct6687-isa-0a20"]["System Fan #6"]["fan8_input"], "{:>.0f} RPM")

SysTempData = _create_sensor_class("SysTempData", lambda d: d["nct6687-isa-0a20"]["System"]["temp2_input"], "{:>.0f}°C")
VrmTempData = _create_sensor_class("VrmTempData", lambda d: d["nct6687-isa-0a20"]["VRM MOS"]["temp3_input"], "{:>.0f}°C")

Ram1Data = _create_sensor_class("Ram1Data", lambda d: d["spd5118-i2c-13-53"]["temp1"]["temp1_input"], "{:>.0f}°C")
Ram2Data = _create_sensor_class("Ram2Data", lambda d: d["spd5118-i2c-13-51"]["temp1"]["temp1_input"], "{:>.0f}°C")

Nvme1Data = _create_sensor_class("Nvme1Data", lambda d: d["nvme-pci-0500"]["Composite"]["temp1_input"], "{:>.0f}°C")
Nvme2Data = _create_sensor_class("Nvme2Data", lambda d: d["nvme-pci-0200"]["Composite"]["temp1_input"], "{:>.0f}°C")
Nvme3Data = _create_sensor_class("Nvme3Data", lambda d: d["nvme-pci-0b00"]["Composite"]["temp1_input"], "{:>.0f}°C")


import psutil

# GPU Power Data
def _fetch_gpu_power(d):
    try:
        import subprocess
        output = subprocess.check_output(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'], text=True)
        return float(output.strip())
    except:
        return 0.0

GpuPowerData = _create_sensor_class("GpuPowerData", _fetch_gpu_power, "{:>.0f}W")

# CPU Thread Data
_cpu_percent_cache = []
_cpu_percent_cache_time = 0

def _get_cpu_percent(thread_id):
    global _cpu_percent_cache, _cpu_percent_cache_time
    import time
    if time.time() - _cpu_percent_cache_time > 1:
        _cpu_percent_cache = psutil.cpu_percent(percpu=True)
        _cpu_percent_cache_time = time.time()
    if thread_id < len(_cpu_percent_cache):
        return _cpu_percent_cache[thread_id]
    return 0.0

for i in range(32):
    globals()[f'CpuThread{i}Data'] = _create_sensor_class(f'CpuThread{i}Data', lambda d, tid=i: _get_cpu_percent(tid), "{:>.0f}%")


# CPU Power Data
_cpu_power_cache_time = 0
_cpu_power_cache_energy = 0
_cpu_power_cache_watts = 0.0

def _fetch_cpu_power(d):
    global _cpu_power_cache_time, _cpu_power_cache_energy, _cpu_power_cache_watts
    import time
    try:
        current_energy = d["zenergy-isa-0000"]["Esocket0"]["energy17_input"]
        current_time = time.time()
        
        if _cpu_power_cache_time > 0 and current_energy >= _cpu_power_cache_energy:
            time_delta = current_time - _cpu_power_cache_time
            if time_delta > 0:
                # energy in Joules, power = J / s = W
                watts = (current_energy - _cpu_power_cache_energy) / time_delta
                _cpu_power_cache_watts = watts
                
        _cpu_power_cache_energy = current_energy
        _cpu_power_cache_time = current_time
        return _cpu_power_cache_watts
    except:
        return 0.0

CpuPowerData = _create_sensor_class("CpuPowerData", _fetch_cpu_power, "{:>.0f}W")

