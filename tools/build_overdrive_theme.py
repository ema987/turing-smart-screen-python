import os
import yaml
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 480
BG_COLOR = (5, 5, 10)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
AMBER = (255, 170, 0)
GRID = (20, 30, 40)
TEXT_WHITE = "255,255,255"

def create_background(out_dir):
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Grid lines
    for x in range(0, WIDTH, 20):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID, width=1)
    for y in range(0, HEIGHT, 20):
        draw.line([(0, y), (WIDTH, y)], fill=GRID, width=1)
        
    try:
        font_l = ImageFont.truetype("../res/fonts/roboto-mono/RobotoMono-Bold.ttf", 30)
        font_s = ImageFont.truetype("../res/fonts/roboto-mono/RobotoMono-Regular.ttf", 18)
    except:
        font_l = ImageFont.load_default()
        font_s = ImageFont.load_default()

    # Define sections
    sections = [
        ("CENTRAL PROCESSING UNIT", 20, CYAN),
        ("GRAPHICS PROCESSING UNIT", 520, CYAN),
        ("MEMORY & NETWORK", 1020, MAGENTA),
        ("COOLING & STORAGE", 1480, AMBER)
    ]
    
    for title, px, color in sections:
        pw = 460 if title != "COOLING & STORAGE" else 420
        draw.rectangle([px, 20, px + pw, HEIGHT - 20], outline=color, width=2)
        draw.rectangle([px, 20, px + pw, 70], fill=color)
        draw.text((px + 20, 30), title, fill=BG_COLOR, font=font_l)
        draw.line([(px + 10, 80), (px + 10, HEIGHT - 30)], fill=color, width=1)
        
    draw.text((60, 210), "THREAD ACTIVITY MATRIX", fill=CYAN, font=font_s)
    draw.text((230, 95), "TOTAL CPU", fill=CYAN, font=font_s)
    draw.rectangle([60, 240, 440, 440], outline=GRID, width=1)
    
    draw.text((560, 210), "VRAM ALLOCATION", fill=CYAN, font=font_s)
    draw.text((560, 320), "GPU POWER", fill=CYAN, font=font_s)
    draw.text((730, 95), "TOTAL GPU", fill=CYAN, font=font_s)
    draw.text((300, 320), "CPU POWER", fill=CYAN, font=font_s)
    
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "background.png"))
    print("Background image generated.")

def add_bg(d):
    """Recursively add BACKGROUND_IMAGE to every dict that has SHOW: True or TEXT or GRAPH"""
    if isinstance(d, dict):
        if "SHOW" in d or "TEXT" in d or "GRAPH" in d:
            d["BACKGROUND_IMAGE"] = "background.png"
        for k, v in d.items():
            add_bg(v)

def generate_yaml(out_dir):
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
        "static_text": {},
        "STATS": {
            "CPU": {
                "PERCENTAGE": {
                    "INTERVAL": 1,
                    "RADIAL": {
                        "SHOW": True, "X": 130, "Y": 140, "RADIUS": 50, "WIDTH": 10,
                        "COLOR": "0,255,255", "BACKGROUND_COLOR": "20,30,40"
                    },
                    "TEXT": {
                        "SHOW": True, "X": 105, "Y": 125, "FONT_SIZE": 30, "FONT_COLOR": TEXT_WHITE,
                        "SHOW_UNIT": True
                    }
                },
                "TEMPERATURE": {
                    "INTERVAL": 1,
                    "LINE_GRAPH": {
                        "SHOW": True, "X": 230, "Y": 130, "WIDTH": 220, "HEIGHT": 60,
                        "COLOR": "0,255,255", "BACKGROUND_COLOR": "0,0,0", "HISTORY_SIZE": 100, "MIN_VALUE": 30, "MAX_VALUE": 95
                    },
                    "TEXT": {
                        "SHOW": True, "X": 230, "Y": 130, "FONT_SIZE": 26, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True
                    }
                }
            },
            "GPU": {
                "PERCENTAGE": {
                    "INTERVAL": 1,
                    "RADIAL": {
                        "SHOW": True, "X": 630, "Y": 140, "RADIUS": 50, "WIDTH": 10,
                        "COLOR": "0,255,255", "BACKGROUND_COLOR": "20,30,40"
                    },
                    "TEXT": {
                        "SHOW": True, "X": 605, "Y": 125, "FONT_SIZE": 30, "FONT_COLOR": TEXT_WHITE,
                        "SHOW_UNIT": True
                    }
                },
                "TEMPERATURE": {
                    "INTERVAL": 1,
                    "LINE_GRAPH": {
                        "SHOW": True, "X": 730, "Y": 130, "WIDTH": 220, "HEIGHT": 60,
                        "COLOR": "0,255,255", "BACKGROUND_COLOR": "0,0,0", "HISTORY_SIZE": 100, "MIN_VALUE": 30, "MAX_VALUE": 90
                    },
                    "TEXT": {
                        "SHOW": True, "X": 730, "Y": 130, "FONT_SIZE": 26, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True
                    }
                },
                "USED_MEMORY": {
                    "INTERVAL": 1,
                    "GRAPH": {
                        "SHOW": True, "X": 560, "Y": 240, "WIDTH": 400, "HEIGHT": 30,
                        "COLOR": "0,255,255", "BACKGROUND_COLOR": "20,30,40"
                    },
                    "PERCENT_TEXT": {
                        "SHOW": True, "X": 560, "Y": 275, "FONT_SIZE": 26, "FONT_COLOR": TEXT_WHITE
                    }
                }
            },
            "MEMORY": {
                "VIRTUAL": {
                    "INTERVAL": 1,
                    "RADIAL": {
                        "SHOW": True, "X": 1130, "Y": 150, "RADIUS": 60, "WIDTH": 12,
                        "COLOR": "255,0,255", "BACKGROUND_COLOR": "20,30,40"
                    },
                    "PERCENT_TEXT": {
                        "SHOW": True, "X": 1105, "Y": 135, "FONT_SIZE": 30, "FONT_COLOR": TEXT_WHITE
                    }
                }
            },
            "NET": {
                "INTERVAL": 1,
                "WLO": {
                    "UPLOAD": {
                        "LINE_GRAPH": {
                            "SHOW": True, "X": 1050, "Y": 250, "WIDTH": 400, "HEIGHT": 60,
                            "COLOR": "255,0,255", "BACKGROUND_COLOR": "0,0,0", "HISTORY_SIZE": 100, "DYNAMIC_MAX_VALUE": True
                        },
                        "TEXT": {
                            "SHOW": True, "X": 1050, "Y": 265, "FONT_SIZE": 24, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True
                        }
                    },
                    "DOWNLOAD": {
                        "LINE_GRAPH": {
                            "SHOW": True, "X": 1050, "Y": 350, "WIDTH": 400, "HEIGHT": 60,
                            "COLOR": "255,0,255", "BACKGROUND_COLOR": "0,0,0", "HISTORY_SIZE": 100, "DYNAMIC_MAX_VALUE": True
                        },
                        "TEXT": {
                            "SHOW": True, "X": 1050, "Y": 365, "FONT_SIZE": 24, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True
                        }
                    }
                }
            },
            "CUSTOM": {
                "INTERVAL": 1,
                "GpuPowerData": {
                    "TEXT": {
                        "SHOW": True, "X": 560, "Y": 350, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True
                    }
                },
                "CpuPowerData": {
                    "TEXT": {
                        "SHOW": True, "X": 300, "Y": 350, "FONT_SIZE": 42, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True
                    }
                }
            }
        }
    }
    
    for i in range(32):
        row = i // 8
        col = i % 8
        theme["STATS"]["CUSTOM"][f"CpuThread{i}Data"] = {
            "GRAPH": {
                "SHOW": True,
                "X": 70 + col * 45,
                "Y": 255 + row * 45,
                "WIDTH": 35,
                "HEIGHT": 35,
                "COLOR": "0,255,255",
                "BACKGROUND_COLOR": "20,30,40"
            }
        }
        
    cooling_list = [
        ("FanCpuData", "CPU FAN", 0), ("FanPumpData", "PUMP FAN", 0), ("FanSys1Data", "SYS1 FAN", 0),
        ("FanSys2Data", "SYS2 FAN", 0), ("FanSys3Data", "SYS3 FAN", 0), ("FanSys6Data", "SYS6 FAN", 0),
        ("SysTempData", "SYS TEMP", 65), ("VrmTempData", "VRM TEMP", 90), 
        ("Ram1Data", "RAM1 TEMP", 60), ("Ram2Data", "RAM2 TEMP", 60),
        ("Nvme1Data", "NVME1 TEMP", 70), ("Nvme2Data", "NVME2 TEMP", 70), ("Nvme3Data", "NVME3 TEMP", 70)
    ]
    
    start_y = 80
    for idx, (sensor, label, crit_val) in enumerate(cooling_list):
        theme["static_text"][f"{sensor}_LBL"] = {
            "TEXT": label,
            "X": 1500, "Y": start_y + idx * 28,
            "FONT_SIZE": 20, "FONT_COLOR": "255,170,0",
            "SHOW": True
        }
        
        sensor_dict = {
            "SHOW": True, "X": 1700, "Y": start_y + idx * 28,
            "FONT_SIZE": 24, "FONT_COLOR": TEXT_WHITE, "SHOW_UNIT": True
        }
        if crit_val > 0:
            sensor_dict["CRITICAL_VALUE"] = crit_val
            sensor_dict["CRITICAL_COLOR"] = "255,0,0"
            
        theme["STATS"]["CUSTOM"][sensor] = {
            "TEXT": sensor_dict
        }
        
    theme["static_text"]["NET_UP_LBL"] = {
        "TEXT": "UPLOAD", "X": 1300, "Y": 220, "FONT_SIZE": 20, "FONT_COLOR": "255,0,255", "SHOW": True
    }
    theme["static_text"]["NET_DN_LBL"] = {
        "TEXT": "DOWNLOAD", "X": 1300, "Y": 320, "FONT_SIZE": 20, "FONT_COLOR": "255,0,255", "SHOW": True
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
