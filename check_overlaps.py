import yaml

with open('res/themes/Overdrive5080/theme.yaml', 'r') as f:
    theme = yaml.safe_load(f)

boxes = []

def parse(d, path=""):
    if isinstance(d, dict):
        if "X" in d and "Y" in d:
            x, y = d["X"], d["Y"]
            w, h = 0, 0
            if "WIDTH" in d and "HEIGHT" in d:
                w, h = d["WIDTH"], d["HEIGHT"]
            elif "RADIUS" in d:
                r = d["RADIUS"]
                x -= r
                y -= r
                w, h = r*2, r*2
            else:
                w, h = 100, 30 # default text bounding box approx
            boxes.append((path, x, y, x+w, y+h))
        for k, v in d.items():
            parse(v, path + "." + k)

parse(theme["STATS"], "STATS")
parse(theme["static_text"], "static_text")

print("Checking overlaps...")
for i, (p1, x1, y1, x2, y2) in enumerate(boxes):
    for j, (p2, a1, b1, a2, b2) in enumerate(boxes):
        if i < j:
            if not (x2 < a1 or x1 > a2 or y2 < b1 or y1 > b2):
                print(f"OVERLAP: {p1} ({x1},{y1}->{x2},{y2}) with {p2} ({a1},{b1}->{a2},{b2})")

