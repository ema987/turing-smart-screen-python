import sys
sys.path.append('.')
import time
from library.sensors.sensors_custom import CpuPowerData

sensor = CpuPowerData()
print("Initial:", sensor.as_numeric())
time.sleep(1.1)
print("After 1s:", sensor.as_numeric())
