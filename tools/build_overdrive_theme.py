import os
import yaml
import subprocess
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 480
BG_COLOR = (5, 5, 10)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
AMBER = (255, 170, 0)
GRID = (20, 30, 40)
TEXT_WHITE = "255,255,255"

def get_sys_names():
    cpu = "AMD Ryzen 9 9950X3D"
    gpu = "NVIDIA GeForce RTX 5080"
    try:
        cpu_raw = subprocess.check_output(["lscpu"]).decode("utf-8")
        for line in cpu_raw.split('\n'):
            if 'Model name' in line:
                cpu = line.split(':')[1].strip().replace(" Processor", "")
                break
    except:
        pass
    
    try:
        gpu = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"]).decode("utf-8").strip()
    except:
        pass
    return cpu, gpu

def create_background(out_dir):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Grid lines
    for x in range(0, WIDTH, 20):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID, width=1)
    for y in range(0, HEIGHT, 20):
        draw.line([(0, y), (WIDTH, y)], fill=GRID, width=1)
        
    try:
        font_l = ImageFont.truetype("res/fonts/roboto-mono/RobotoMono-Bold.ttf", 35)
    except:
        font_l = ImageFont.load_default()

    # Define sections - EVENLY SPACED 450px WIDTH, 24px GAPS
    sections = [
        ("CPU", 24, CYAN),
        ("GPU", 498, CYAN),
        ("MEMORY", 972, MAGENTA),
        ("TEMPERATURES", 1446, AMBER)
    ]
    
    for title, px, color in sections:
        pw = 450
        draw.rectangle([px, 20, px + pw, HEIGHT - 20], outline=color, width=2)
        draw.rectangle([px, 20, px + pw, 70], fill=color)
        draw.text((px + 20, 25), title, fill=BG_COLOR, font=font_l)
        
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "background.png"))
    print("Background image generated.")

def add_bg(d):
    if isinstance(d, dict):
        if "SHOW" in d or "TEXT" in d or "GRAPH" in d:
            d["BACKGROUND_IMAGE"] = "background.png"
        for k, v in d.items():
            add_bg(v)

def generate_yaml(out_dir):
    cpu_name, gpu_name = get_sys_names()
    
    theme = {
        "display": {
            "DISPLAY_ORIENTATION": "landscape",
            "DISPLAY_SIZE": "8.8\"", 
            "DISPLAY_REVERSE": False
        },
        "static_images": {
            "BACKGROUND": {
                "PATH": "background.png",
                "X": 0, "Y": 0, "WIDTH": WIDTH, "HEIGHT": HEIGHT
            }
        },
        "static_text": {
            # CPU PANE: 24 to 474
            "CPU_NAME": {"TEXT": cpu_name, "X": 44, "Y": 80, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True},
            "CPU_USAGE_LBL": {"TEXT": "CPU USAGE", "X": 44, "Y": 130, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True},
            "CPU_TEMP_LBL": {"TEXT": "CPU TEMP", "X": 454, "Y": 130, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True, "ALIGN": "right", "ANCHOR": "rt"},
            "CPU_CLOCK_LBL": {"TEXT": "CORE CLOCK", "X": 44, "Y": 250, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True},
            "CPU_POWER_LBL": {"TEXT": "CPU POWER", "X": 454, "Y": 250, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True, "ALIGN": "right", "ANCHOR": "rt"},
            
            # GPU PANE: 498 to 948
            "GPU_NAME": {"TEXT": gpu_name, "X": 518, "Y": 80, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True},
            "GPU_USAGE_LBL": {"TEXT": "GPU USAGE", "X": 518, "Y": 130, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True},
            "GPU_TEMP_LBL": {"TEXT": "GPU TEMP", "X": 928, "Y": 130, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True, "ALIGN": "right", "ANCHOR": "rt"},
            "GPU_CLOCK_LBL": {"TEXT": "CORE CLOCK", "X": 518, "Y": 250, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True},
            "GPU_POWER_LBL": {"TEXT": "GPU POWER", "X": 928, "Y": 250, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True, "ALIGN": "right", "ANCHOR": "rt"},
            "VRAM_LBL": {"TEXT": "VRAM ALLOCATED", "X": 518, "Y": 370, "FONT_SIZE": 20, "FONT_COLOR": "0,255,255", "SHOW": True},
            
            # MEMORY PANE: 972 to 1422
            "SYS_MEM_NAME": {"TEXT": "SYSTEM MEMORY", "X": 992, "Y": 80, "FONT_SIZE": 20, "FONT_COLOR": "255,0,255", "SHOW": True},
            "RAM_SPECS_LBL": {"TEXT": "6000 MT/s CL40", "X": 1402, "Y": 80, "FONT_SIZE": 20, "FONT_COLOR": "255,0,255", "SHOW": True, "ALIGN": "right", "ANCHOR": "rt"},
            "RAM_ALLOC_LBL": {"TEXT": "ALLOCATED", "X": 992, "Y": 130, "FONT_SIZE": 20, "FONT_COLOR": "255,0,255", "SHOW": True},
            "RAM_FREE_LBL": {"TEXT": "FREE", "X": 992, "Y": 250, "FONT_SIZE": 20, "FONT_COLOR": "255,0,255", "SHOW": True},
            "RAM_TOTAL_LBL": {"TEXT": "TOTAL", "X": 992, "Y": 370, "FONT_SIZE": 20, "FONT_COLOR": "255,0,255", "SHOW": True},
        },
        "STATS": {
            "CPU": {
                "PERCENTAGE": {
                    "INTERVAL": 1,
                    "TEXT": {"SHOW": True, "X": 44, "Y": 160, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True}
                },
                "TEMPERATURE": {
                    "INTERVAL": 1,
                    "TEXT": {"SHOW": True, "X": 254, "Y": 160, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True, "CRITICAL_VALUE": 70, "CRITICAL_COLOR": "255,0,0", "ALIGN": "right", "ANCHOR": "rt"}
                },
                "FREQUENCY": {
                    "INTERVAL": 1,
                    "TEXT": {"SHOW": True, "X": 44, "Y": 280, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True, "UNIT": " GHz"}
                }
            },
            "GPU": {
                "INTERVAL": 1,
                "SHOW": True,
                "PERCENTAGE": {
                    "INTERVAL": 1,
                    "TEXT": {"SHOW": True, "X": 518, "Y": 160, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True}
                },
                "TEMPERATURE": {
                    "INTERVAL": 1,
                    "TEXT": {"SHOW": True, "X": 728, "Y": 160, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True, "CRITICAL_VALUE": 70, "CRITICAL_COLOR": "255,0,0", "ALIGN": "right", "ANCHOR": "rt"}
                },
                "FREQUENCY": {
                    "INTERVAL": 1,
                    "TEXT": {"SHOW": True, "X": 518, "Y": 280, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True, "UNIT": " GHz"}
                },
                "MEMORY_USED": {
                    "INTERVAL": 1,
                    "TEXT": {"SHOW": True, "X": 518, "Y": 400, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True}
                }
            },
            "MEMORY": {
                "INTERVAL": 1,
                "VIRTUAL": {
                    "INTERVAL": 1,
                    "USED": {"SHOW": True, "X": 992, "Y": 160, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True},
                    "FREE": {"SHOW": True, "X": 992, "Y": 280, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True},
                    "TOTAL": {"SHOW": True, "X": 992, "Y": 400, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True}
                }
            },
            "CUSTOM": {
                "INTERVAL": 1,
                "CpuPowerData": {
                    "TEXT": {"SHOW": True, "X": 254, "Y": 280, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True, "ALIGN": "right", "ANCHOR": "rt"}
                },
                "GpuPowerData": {
                    "TEXT": {"SHOW": True, "X": 728, "Y": 280, "WIDTH": 200, "HEIGHT": 60, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True, "ALIGN": "right", "ANCHOR": "rt"}
                }
            }
        }
    }
    
    # TEMPERATURES PANE: 1446 to 1896
    cooling_list = [
        ("FanCpuData", "CPU FAN", 0), ("FanPumpData", "PUMP FAN", 0), ("FanSys1Data", "SYS1 FAN", 0),
        ("FanSys2Data", "SYS2 FAN", 0), ("FanSys3Data", "SYS3 FAN", 0), ("FanSys6Data", "SYS6 FAN", 0),
        ("SysTempData", "SYS TEMP", 55), ("VrmTempData", "VRM TEMP", 55), 
        ("Ram1Data", "RAM1 TEMP", 55), ("Ram2Data", "RAM2 TEMP", 55),
        ("Nvme1Data", "NVME1 TEMP", 50), ("Nvme2Data", "NVME2 TEMP", 50), ("Nvme3Data", "NVME3 TEMP", 50)
    ]
    
    start_y = 80
    for idx, (sensor, label, crit_val) in enumerate(cooling_list):
        theme["static_text"][f"{sensor}_LBL"] = {
            "TEXT": label,
            "X": 1466, "Y": start_y + idx * 28,
            "FONT_SIZE": 20, "FONT_COLOR": "255,170,0",
            "SHOW": True
        }
        
        sensor_dict = {
            "SHOW": True, "X": 1666, "Y": start_y + idx * 28,
            "WIDTH": 200, "HEIGHT": 28,
            "FONT_SIZE": 24, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True
        }
        if crit_val > 0:
            sensor_dict["CRITICAL_VALUE"] = crit_val
            sensor_dict["CRITICAL_COLOR"] = "255,0,0"
            
        theme["STATS"]["CUSTOM"][sensor] = {
            "TEXT": sensor_dict
        }

    # INJECT BACKGROUND_IMAGE TO EVERYTHING
    add_bg(theme)

    with open(os.path.join(out_dir, "theme.yaml"), "w") as f:
        yaml.dump(theme, f, sort_keys=False)
    print("theme.yaml generated.")

if __name__ == "__main__":
    out = "res/themes/Overdrive5080"
    create_background(out)
    generate_yaml(out)
