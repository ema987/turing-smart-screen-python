import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1920
HEIGHT = 480
BG_COLOR = (10, 15, 25)
NEON_CYAN = (0, 255, 255)
NEON_MAGENTA = (255, 0, 255)
DIM_CYAN = (0, 100, 100)
DIM_MAGENTA = (100, 0, 100)
GRID_COLOR = (20, 35, 50)

def draw_hud():
    img = Image.new('RGB', (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw grid
    for x in range(0, WIDTH, 40):
        draw.line([(x, 0), (x, HEIGHT)], fill=GRID_COLOR, width=1)
    for y in range(0, HEIGHT, 40):
        draw.line([(0, y), (WIDTH, y)], fill=GRID_COLOR, width=1)

    margin = 20
    panel_w = 455
    spacing = 20
    
    # Titles
    titles = [
        ("CENTRAL PROCESSING UNIT", NEON_CYAN, 20),
        ("GRAPHICS PROCESSING UNIT", NEON_CYAN, 20 + panel_w + spacing),
        ("COOLING SYSTEMS", NEON_CYAN, 20 + (panel_w + spacing)*2),
        ("MOTHERBOARD & STORAGE", NEON_MAGENTA, 20 + (panel_w + spacing)*3)
    ]
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("../res/fonts/roboto-mono/RobotoMono-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()

    for idx in range(4):
        px = 20 + idx * (panel_w + spacing)
        py = 20
        color = NEON_MAGENTA if idx == 3 else NEON_CYAN
        dim_color = DIM_MAGENTA if idx == 3 else DIM_CYAN
        
        # Draw panel outline
        # Corners cut
        corner = 30
        points = [
            (px + corner, py),
            (px + panel_w, py),
            (px + panel_w, py + 440 - corner),
            (px + panel_w - corner, py + 440),
            (px, py + 440),
            (px, py + corner)
        ]
        draw.polygon(points, outline=color, width=2)
        
        # Inner accent lines
        draw.line([(px + 10, py + 10 + corner), (px + 10, py + 440 - 10)], fill=dim_color, width=1)
        
        # Title
        title_text, title_col, title_x = titles[idx]
        draw.text((px + 40, py + 15), title_text, fill=title_col, font=font)
        draw.line([(px + 40, py + 45), (px + panel_w - 20, py + 45)], fill=dim_color, width=1)

    # Specific grid elements for graphs (CPU and GPU)
    for idx in [0, 1]:
        px = 20 + idx * (panel_w + spacing)
        gx = px + 40
        gy = 280
        gw = panel_w - 60
        gh = 130
        draw.rectangle([gx, gy, gx + gw, gy + gh], outline=DIM_CYAN, width=1)
        # graph grid
        for i in range(1, 4):
            draw.line([(gx, gy + i*32.5), (gx + gw, gy + i*32.5)], fill=(20, 40, 60), width=1)

    # Save
    out_dir = "../res/themes/Cyberpunk9Inch"
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "background.png"))
    print("Background created successfully.")

if __name__ == "__main__":
    draw_hud()
