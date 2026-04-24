import numpy as np
import cv2
import csv
import glob


files = glob.glob("*.jpg") + glob.glob("*.png") + glob.glob("*.jpeg")
img = cv2.imread(files[0])

line_color = []

def color_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        line_color.append(img[y, x])

img_copy = img.copy()
cv2.putText(img_copy, "Click on the line color", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.imshow("image", img_copy)
cv2.setMouseCallback("image", color_click)

while not line_color:
    cv2.waitKey(1)
cv2.destroyAllWindows()

target_blue = line_color[0][0]
target_red = line_color[0][2]

target = line_color[0]

diff = img.astype(int) - target
distance = np.sqrt(np.sum(diff**2, axis=2))
mask = distance < 30

xs = []
ys = []

rows, cols = np.where(mask)


unique_cols = np.unique(cols)

for col in unique_cols:
    matching_row = rows[col == cols]
    one_row = np.mean(matching_row)
    xs.append(col)
    ys.append(one_row)

points = []

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 2:
            points.append((x,y))


img_copy2 = img.copy()
cv2.putText(img_copy2, "Click bottom-left then top-right corner", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.imshow("image", img_copy2)
cv2.setMouseCallback("image", click)

while len(points) < 2:
    cv2.waitKey(1)
cv2.destroyAllWindows()
print(f"Starting coords:{points[0]}, Ending coords:{points[1]}")

x_min = float(input("x min: "))
x_max = float(input("x max: "))
y_min = float(input("y min: "))
y_max = float(input("y max: "))

x_start, y_start = points[0]
x_end, y_end = points[1]

x_save = []
y_save = []



for i in range(len(xs)):
    pixel_col = xs[i]
    pixel_row = ys[i]
    real_x = x_min + (pixel_col - x_start) / (x_end - x_start) * (x_max - x_min)
    real_y = y_min + (y_start - pixel_row) / (y_start - y_end) * (y_max - y_min)
    x_save.append(real_x)
    y_save.append(real_y)

num_points = int(input("How many points do you want: "))

indices = np.linspace(0, len(x_save)-1, num_points).astype(int)

with open('graph.csv', 'w', newline="") as file:
    try:
        writer = csv.writer(file)
        writer.writerow(["x", "y"])
        for i in indices:
            writer.writerow([x_save[i], y_save[i]])
    except:
        print("The process failed!")
    print("File created successfully!")

