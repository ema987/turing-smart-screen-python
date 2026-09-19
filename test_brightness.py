from PIL import Image
import numpy as np

img = Image.open("res/themes/Overdrive5080/background.png").convert('L')
img = img.resize((1920, 1920))
arr = np.array(img)

best_top = 0
best_avg = 0
for t in range(0, 1920 - 480, 50):
    slice_arr = arr[t:t+480, :]
    avg = np.mean(slice_arr)
    if avg > best_avg:
        best_avg = avg
        best_top = t
    print(f"Top: {t}, Avg Brightness: {avg:.2f}")

print(f"Best Top: {best_top} with Avg Brightness: {best_avg:.2f}")
