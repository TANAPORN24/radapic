import requests
from bs4 import BeautifulSoup
import os
import re
from PIL import Image
import numpy as np
import os
import shutil

drive_folder = "/content/drive/My Drive/Radar_Output"
os.makedirs(drive_folder, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

# === STEP 1: ดึงภาพ GIF จากเว็บไซต์ ===

# URL ของหน้าที่มี GIF
url = "https://weather.tmd.go.th/skn240_HQ_edit2.php"

# กำหนดโฟลเดอร์เก็บไฟล์
input_folder = "input"
output_folder = "output"
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# ดึงหน้าเว็บ
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# ค้นหา URL ของไฟล์ GIF
gif_url = None
for img in soup.find_all("img"):
    if ".gif" in img["src"]:
        gif_url = img["src"]
        break  # เอาไฟล์แรกที่เจอ

if gif_url:
    # ตรวจสอบว่า URL เป็นแบบเต็มหรือไม่
    if not gif_url.startswith("http"):
        gif_url = "https://weather.tmd.go.th/" + gif_url

    print(f"✅ พบไฟล์ GIF: {gif_url}")

    # หาหมายเลขไฟล์ถัดไป
    existing_files = os.listdir(input_folder)
    max_index = 0
    pattern = re.compile(r"skn240_HQ_latest \((\d+)\)\.gif")
    for file in existing_files:
        match = pattern.match(file)
        if match:
            file_index = int(match.group(1))
            max_index = max(max_index, file_index)

    next_index = max_index + 1
    gif_filename = f"skn240_HQ_latest ({next_index}).gif"
    gif_path = os.path.join(input_folder, gif_filename)

    # ดาวน์โหลด GIF
    gif_response = requests.get(gif_url, stream=True)
    with open(gif_path, "wb") as file:
        for chunk in gif_response.iter_content(chunk_size=1024):
            file.write(chunk)

    print(f"✅ ไฟล์ GIF ถูกบันทึกที่: {gif_path}")

    # === STEP 2: ลบพื้นหลังและตัดภาพ ===

    # โหลดภาพ GIF
    image = Image.open(gif_path).convert("RGBA")
    image_data = np.array(image)

    # ฟังก์ชันตรวจสอบสีของเรดาร์
    def is_rain_data(pixel):
        r, g, b, a = pixel
        return not (40 < r < 180 and 60 < g < 200 and 40 < b < 180)

    # สร้าง mask เพื่อลบพื้นหลัง
    mask = np.apply_along_axis(is_rain_data, -1, image_data)
    image_data[~mask] = [0, 0, 0, 0]  # ทำให้พื้นที่ไม่ใช่เรดาร์เป็นโปร่งใส

    # กำจัดสีฟ้าและสีขาวที่อาจหลงเหลือ
    blue_lower = np.array([0, 0, 100, 0])
    blue_upper = np.array([100, 255, 255, 255])
    white_lower = np.array([200, 200, 200, 0])
    white_upper = np.array([255, 255, 255, 255])

    blue_mask = ((image_data[:, :, 0] >= blue_lower[0]) & (image_data[:, :, 0] <= blue_upper[0]) &
                 (image_data[:, :, 1] >= blue_lower[1]) & (image_data[:, :, 1] <= blue_upper[1]) &
                 (image_data[:, :, 2] >= blue_lower[2]) & (image_data[:, :, 2] <= blue_upper[2]))

    white_mask = ((image_data[:, :, 0] >= white_lower[0]) & (image_data[:, :, 0] <= white_upper[0]) &
                  (image_data[:, :, 1] >= white_lower[1]) & (image_data[:, :, 1] <= white_upper[1]) &
                  (image_data[:, :, 2] >= white_lower[2]) & (image_data[:, :, 2] <= white_upper[2]))

    final_mask = blue_mask | white_mask
    image_data[final_mask] = [0, 0, 0, 0]  # ทำให้สีที่ไม่ต้องการโปร่งใส

    # แปลงกลับเป็นภาพ
    processed_image = Image.fromarray(image_data)

    # ตัดขนาดภาพให้เหลือ 1745x1585 พิกเซล (ชิดขวาบน)
    crop_width, crop_height = 1745, 1585
    orig_width, orig_height = processed_image.size
    left, upper = orig_width - crop_width, 0
    right, lower = orig_width, crop_height
    cropped_image = processed_image.crop((left, upper, right, lower))

    # ครอปรูปเป็นวงกลม
    width, height = cropped_image.size
    center_x, center_y = width // 2, height // 2
    radius = 792

    mask = Image.new("L", (width, height), 0)
    mask_data = np.array(mask)
    y, x = np.ogrid[:height, :width]
    mask_area = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
    mask_data[mask_area] = 255
    circular_mask = Image.fromarray(mask_data, mode="L")

    circular_rain_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    circular_rain_image.paste(cropped_image, (0, 0), circular_mask)

    # บันทึกภาพที่ได้
    output_filename = f"skn240_HQ_latest ({next_index}).png"
    output_path = os.path.join(output_folder, output_filename)
    circular_rain_image.save(output_path)

    print(f"✅ บันทึกภาพเรดาร์ที่ประมวลผลแล้วที่: {output_path}")
else:
    print("❌ ไม่พบไฟล์ GIF ในหน้าเว็บ")

# ลบไฟล์ทั้งหมดในโฟลเดอร์ input
for file in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file)
    try:
        os.remove(file_path)  # ลบไฟล์ทีละไฟล์
    except Exception as e:
        print(f"❌ ไม่สามารถลบ {file_path}: {e}")

print("✅ ล้างข้อมูลในโฟลเดอร์ input แล้ว")
