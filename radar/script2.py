import requests
from bs4 import BeautifulSoup
import os

# URL ของหน้าที่มี GIF
url = "https://weather.tmd.go.th/skn240_HQ_edit2.php"

# ส่ง HTTP request เพื่อดึงหน้าเว็บ
response = requests.get(url)
response.raise_for_status()  # ตรวจสอบว่าดาวน์โหลดสำเร็จ

# ใช้ BeautifulSoup เพื่อดึงลิงก์ของไฟล์ GIF
soup = BeautifulSoup(response.text, "html.parser")
gif_url = None

# ค้นหาแท็ก <img> ที่มีไฟล์ .gif
for img in soup.find_all("img"):
    if ".gif" in img["src"]:
        gif_url = img["src"]
        break  # เอาไฟล์แรกที่เจอ

# ตรวจสอบว่าพบลิงก์ GIF หรือไม่
if gif_url:
    # ทำให้ URL เป็นแบบเต็มถ้าเป็น relative path
    if not gif_url.startswith("http"):
        gif_url = "https://weather.tmd.go.th/" + gif_url

    print(f"✅ พบไฟล์ GIF: {gif_url}")

    # ตั้งค่าพาธบันทึกไฟล์
    output_folder = "input"
    os.makedirs(output_folder, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี
    file_name = os.path.join(output_folder, os.path.basename(gif_url))  # เก็บชื่อไฟล์จาก URL

    # ดาวน์โหลดไฟล์ GIF
    gif_response = requests.get(gif_url, stream=True)
    with open(file_name, "wb") as file:
        for chunk in gif_response.iter_content(chunk_size=1024):
            file.write(chunk)

    print(f"✅ ไฟล์ GIF ถูกบันทึกที่: {file_name}")

else:
    print("❌ ไม่พบไฟล์ GIF ในหน้าเว็บ")
