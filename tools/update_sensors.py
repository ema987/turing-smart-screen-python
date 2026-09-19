import sys

content = """
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

"""

with open("library/sensors/sensors_custom.py", "a") as f:
    f.write(content)
