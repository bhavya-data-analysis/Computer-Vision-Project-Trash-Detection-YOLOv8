import os

IMAGE_DIR = "images"
LABEL_DIR = "labels"

images = sorted([
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

for idx, img_name in enumerate(images, start=1):
    new_base = f"{idx:03d}"

    old_img_path = os.path.join(IMAGE_DIR, img_name)
    new_img_path = os.path.join(IMAGE_DIR, new_base + ".jpg")

    os.rename(old_img_path, new_img_path)

    old_label = os.path.splitext(img_name)[0] + ".txt"
    old_label_path = os.path.join(LABEL_DIR, old_label)

    if os.path.exists(old_label_path):
        new_label_path = os.path.join(LABEL_DIR, new_base + ".txt")
        os.rename(old_label_path, new_label_path)
