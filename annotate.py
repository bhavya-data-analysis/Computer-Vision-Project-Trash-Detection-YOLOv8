import cv2
import os
from PIL import Image
import pillow_heif
import numpy as np

IMAGE_DIR = "images"
LABEL_DIR = "labels"
os.makedirs(LABEL_DIR, exist_ok=True)

images = sorted(os.listdir(IMAGE_DIR))

for img_name in images:
    ext = img_name.lower()

    if not ext.endswith((".jpg", ".jpeg", ".png", ".heic")):
        continue

    label_path = os.path.join(
        LABEL_DIR, os.path.splitext(img_name)[0] + ".txt"
    )

    if os.path.exists(label_path):
        continue

    img_path = os.path.join(IMAGE_DIR, img_name)

    # ---- LOAD IMAGE (HEIC or normal) ----
    if ext.endswith(".heic"):
        heif = pillow_heif.open_heif(img_path)
        pil_img = Image.frombytes(
            heif.mode,
            heif.size,
            heif.data,
            "raw"
        )
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    else:
        img = cv2.imread(img_path)

    if img is None:
        continue

    # ---- DRAW BOX ----
    bbox = cv2.selectROI(f"Draw box: {img_name}", img, False)
    cv2.destroyAllWindows()

    x, y, bw, bh = bbox
    if bw == 0 or bh == 0:
        continue

    h, w, _ = img.shape

    xc = (x + bw / 2) / w
    yc = (y + bh / 2) / h
    bw /= w
    bh /= h

    with open(label_path, "w") as f:
        f.write(f"0 {xc} {yc} {bw} {bh}")

    print(f"Labeled {img_name}")
