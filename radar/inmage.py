# # import cv2
# # import numpy as np
# # from matplotlib import pyplot as plt

# # def convert_to_blue_yellow(image_path, output_path):
# #     # โหลดภาพ
# #     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# #     # แปลงภาพเป็นสีน้ำเงินและเหลือง
# #     blue_yellow_image = np.zeros_like(image)

# #     # ย้อมสีภาพให้เป็นสีน้ำเงิน
# #     blue_yellow_image[:, :, 0] = image[:, :, 0]  # สีน้ำเงิน (B)
# #     blue_yellow_image[:, :, 1] = image[:, :, 1] * 0.5  # สีเขียว (G) ลดความเข้มลง
# #     blue_yellow_image[:, :, 2] = image[:, :, 2]  # สีแดง (R) ลดความเข้มลง

# #     # บันทึกผลลัพธ์
# #     cv2.imwrite(output_path, blue_yellow_image)

# #     # แสดงภาพ
# #     plt.figure(figsize=(8, 8))
# #     plt.imshow(cv2.cvtColor(blue_yellow_image, cv2.COLOR_BGR2RGB))  # แสดงภาพใน RGB
# #     plt.axis("off")
# #     plt.show()

# #     return output_path

# # # ตัวอย่างการใช้งาน
# # image_path = "srt240_latest.jpg"  # เปลี่ยนเป็นไฟล์ของคุณ
# # output_path = "output_blue_yellow.png"
# # convert_to_blue_yellow(image_path, output_path)

# # import cv2
# # import numpy as np
# # from matplotlib import pyplot as plt

# # def separate_green(image_path, output_path):
# #     # โหลดภาพ
# #     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# #     # สร้างภาพใหม่สำหรับสีเขียวธรรมดาและเขียวสว่าง
# #     green_normal = np.zeros_like(image)
# #     green_bright = np.zeros_like(image)

# #     # เงื่อนไขในการแยกสีเขียวธรรมดาและเขียวสว่าง
# #     for i in range(image.shape[0]):
# #         for j in range(image.shape[1]):
# #             b, g, r = image[i, j]

# #             # สีเขียวธรรมดา
# #             if g >= 80 and g <= 150 and r < 100 and b < 100:  # ปรับเกณฑ์
# #                 green_normal[i, j] = [0, 255, 0]  # ย้อมสีเขียวธรรมดาเป็นสีเขียวสด

# #             # สีเขียวสว่าง
# #             elif g > 150:  # สีเขียวที่สว่างมาก
# #                 green_bright[i, j] = [255, 255, 0]  # ย้อมสีเขียวสว่างเป็นสีเหลือง

# #     # บันทึกผลลัพธ์
# #     cv2.imwrite(output_path + "_green_normal.png", green_normal)
# #     cv2.imwrite(output_path + "_green_bright.png", green_bright)

# #     # แสดงภาพ
# #     plt.figure(figsize=(12, 6))

# #     plt.subplot(1, 2, 1)
# #     plt.imshow(cv2.cvtColor(green_normal, cv2.COLOR_BGR2RGB))
# #     plt.title('Green Normal')
# #     plt.axis("off")

# #     plt.subplot(1, 2, 2)
# #     plt.imshow(cv2.cvtColor(green_bright, cv2.COLOR_BGR2RGB))
# #     plt.title('Green Bright')
# #     plt.axis("off")

# #     plt.show()

# # # ตัวอย่างการใช้งาน
# # image_path = "output_blue_yellow.png"  # เปลี่ยนเป็นไฟล์ของคุณ
# # output_path = "output_separated_green"
# # separate_green(image_path, output_path)

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # โหลดภาพที่อัปโหลด
# image_path = "output_blue_yellow.png"
# image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# # ตรวจสอบว่าภาพโหลดสำเร็จหรือไม่
# if image is None:
#     raise ValueError("ไม่สามารถโหลดภาพได้ ตรวจสอบพาธไฟล์")

# # แปลงภาพจาก RGBA เป็น BGR โดยตัดช่อง Alpha ออก
# image_bgr = image[:, :, :3]

# # แยกภาพตามสีที่กำหนด (แก้ไขใหม่ให้รองรับ BGR)
# color_ranges_bgr = {
#     "red": ((0, 0, 150), (100, 100, 255)),
#     "orange": ((0, 50, 150), (100, 150, 255)),
#     "yellow": ((0, 150, 150), (100, 255, 255)),
#     "green_light": ((100, 200, 100), (150, 255, 150)),
#     "green_dark": ((0, 100, 0), (100, 200, 100)),
#     "blue": ((150, 100, 0), (255, 150, 100)),
#     "purple": ((150, 0, 150), (255, 100, 255))
# }

# # แยกสีในภาพใหม่
# separated_images_bgr = {}

# for color, (lower, upper) in color_ranges_bgr.items():
#     lower = np.array(lower, dtype=np.uint8)
#     upper = np.array(upper, dtype=np.uint8)

#     mask = cv2.inRange(image_bgr, lower, upper)
#     result = cv2.bitwise_and(image_bgr, image_bgr, mask=mask)
#     separated_images_bgr[color] = result

# # แสดงผลลัพธ์
# plt.figure(figsize=(12, 8))

# for i, (color, img) in enumerate(separated_images_bgr.items()):
#     plt.subplot(3, 3, i + 1)
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.title(color)
#     plt.axis("off")

# plt.tight_layout()
# plt.show()

# # บันทึกผลลัพธ์ใหม่
# output_paths_bgr = {}
# for color, img in separated_images_bgr.items():
#     output_path = f"/mnt/data/separated_{color}.png"
#     cv2.imwrite(output_path, img)
#     output_paths_bgr[color] = output_path

# output_paths_bgr




#------------------------------------------------ตัวหลัก------------------------------------------------------------
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # โหลดภาพที่อัปโหลด
# image_path = "radar/srt240_latest.jpg"  # เปลี่ยนเป็นพาธของภาพที่คุณใช้
# image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# # ตรวจสอบว่าภาพโหลดสำเร็จหรือไม่
# if image is None:
#     raise ValueError("ไม่สามารถโหลดภาพได้ ตรวจสอบพาธไฟล์")

# # แปลงภาพจาก RGBA เป็น BGR โดยตัดช่อง Alpha ออก
# image_bgr = image[:, :, :3]

# # กำหนดช่วงสีที่ต้องการแยก (BGR)
# color_ranges_bgr = {
#     "red": ((0, 0, 150), (100, 100, 255)),
#     "orange": ((0, 50, 150), (100, 150, 255)),
#     "yellow": ((0, 150, 150), (100, 255, 255)),
#     "green_light": ((100, 200, 100), (150, 255, 150)),
#     "green_dark": ((0, 100, 0), (100, 200, 100))
# }

# # สร้างภาพเปล่าขนาดเท่ากับภาพต้นฉบับ
# composite_image = np.zeros_like(image_bgr)

# # วนลูปแยกสีและรวมภาพ
# for color, (lower, upper) in color_ranges_bgr.items():
#     lower = np.array(lower, dtype=np.uint8)
#     upper = np.array(upper, dtype=np.uint8)

#     # สร้าง Mask สำหรับสีที่กำหนด
#     mask = cv2.inRange(image_bgr, lower, upper)
    
#     # ใช้ Mask ในการดึงเฉพาะสีที่ต้องการ
#     extracted_color = cv2.bitwise_and(image_bgr, image_bgr, mask=mask)

#     # รวมภาพโดยใช้ cv2.add()
#     composite_image = cv2.add(composite_image, extracted_color)

# # แสดงภาพที่รวมกันแล้ว
# plt.figure(figsize=(6, 6))
# plt.imshow(cv2.cvtColor(composite_image, cv2.COLOR_BGR2RGB))
# plt.title("Composite Image")
# plt.axis("off")
# plt.show()

# # บันทึกผลลัพธ์
# output_composite_path = "15.png"
# cv2.imwrite(output_composite_path, composite_image)

# print(f"ดาวน์โหลดภาพที่รวมกันได้ที่: {output_composite_path}")
#------------------------------------------------ตัวหลัก------------------------------------------------------------
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # โหลดภาพที่อัปโหลด
# image_path = "radar/srt240_latest.jpg"  # เปลี่ยนเป็นพาธของภาพที่คุณใช้
# image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# # ตรวจสอบว่าภาพโหลดสำเร็จหรือไม่
# if image is None:
#     raise ValueError("ไม่สามารถโหลดภาพได้ ตรวจสอบพาธไฟล์")

# # แปลงภาพจาก BGR เป็น HSV
# image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # กำหนดช่วงสีที่ต้องการเก็บไว้โดยใช้ค่าประมาณ
# color_ranges_hsv = [
#     ((0, 50, 50), (10, 255, 255)),   # แดง
#     ((10, 100, 100), (25, 255, 255)), # ส้ม
#     ((25, 100, 100), (35, 255, 255)), # เหลือง
#     ((35, 50, 50), (85, 255, 255)),  # เขียว
#     ((85, 50, 50), (125, 255, 255))  # ฟ้า
# ]

# # สร้าง mask ว่างสำหรับเก็บผลรวมของ mask
# mask_total = np.zeros(image_hsv.shape[:2], dtype=np.uint8)

# # วนลูปเพื่อสร้าง mask สำหรับช่วงสีที่ต้องการเก็บไว้
# for lower, upper in color_ranges_hsv:
#     lower = np.array(lower, dtype=np.uint8)
#     upper = np.array(upper, dtype=np.uint8)
#     mask = cv2.inRange(image_hsv, lower, upper)
#     mask_total = cv2.bitwise_or(mask_total, mask)

# # ใช้ Mask ในการดึงเฉพาะสีที่ต้องการ
# filtered_image = cv2.bitwise_and(image, image, mask=mask_total)

# # แสดงภาพที่ผ่านการกรอง
# plt.figure(figsize=(6, 6))
# plt.imshow(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB))
# plt.title("Filtered Image")
# plt.axis("off")
# plt.show()

# # บันทึกผลลัพธ์
# output_filtered_path = "filtered_image.png"
# cv2.imwrite(output_filtered_path, filtered_image)

# print(f"ดาวน์โหลดภาพที่ผ่านการกรองได้ที่: {output_filtered_path}")


#------------------------------------------------------จัดอันดับสีแล้วลบ------------------------------------------------------#
import cv2
import numpy as np
from collections import Counter

# โหลดภาพ
image_path = "output2.png"  # เปลี่ยนเป็นพาธของคุณ
image = cv2.imread(image_path)

# แปลงเป็น RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# รีเชพเป็น list ของพิกเซล
pixels = image_rgb.reshape(-1, 3)

# นับจำนวนพิกเซลแต่ละสี
color_counts = Counter(map(tuple, pixels))

# ดึงสีที่พบบ่อยที่สุด 5 อันดับ
most_common_colors = color_counts.most_common(5)
print("Top 5 colors:", most_common_colors)

# สร้าง mask สำหรับสีที่ต้องการลบ
mask = np.zeros(image.shape[:2], dtype=np.uint8)

for color, _ in most_common_colors:
    lower = np.array(color) - 10  # เผื่อช่วงสี
    upper = np.array(color) + 10
    mask |= cv2.inRange(image_rgb, lower, upper)

# ลบสีโดยเปลี่ยนเป็นสีขาว
image_rgb[mask > 0] = [255, 255, 255]

# บันทึกผลลัพธ์
cv2.imwrite("output3.png", cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))


#------------------------------------------------------จัดอันดับสีแล้วลบ------------------------------------------------------#


# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # โหลดภาพที่อัปโหลด
# image_path = "radar/srt240_latest.jpg"  # เปลี่ยนเป็นพาธของภาพที่คุณใช้
# image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# # ตรวจสอบว่าภาพโหลดสำเร็จหรือไม่
# if image is None:
#     raise ValueError("ไม่สามารถโหลดภาพได้ ตรวจสอบพาธไฟล์")

# # ฟังก์ชันสำหรับการกรองสี
# def filter_colors(image):
#     # แปลงภาพจาก BGR เป็น HSV
#     image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # กำหนดช่วงสีที่ต้องการเก็บไว้โดยใช้ค่าประมาณ
#     color_ranges_hsv = [
#         ((0, 50, 50), (10, 255, 255)),   # แดง
#         ((10, 100, 100), (25, 255, 255)), # ส้ม
#         ((25, 100, 100), (35, 255, 255)), # เหลือง
#         ((35, 50, 50), (85, 255, 255)),  # เขียว
#         ((85, 50, 50), (125, 255, 255))  # ฟ้า
#     ]

#     # สร้าง mask ว่างสำหรับเก็บผลรวมของ mask
#     mask_total = np.zeros(image_hsv.shape[:2], dtype=np.uint8)

#     # วนลูปเพื่อสร้าง mask สำหรับช่วงสีที่ต้องการเก็บไว้
#     for lower, upper in color_ranges_hsv:
#         lower = np.array(lower, dtype=np.uint8)
#         upper = np.array(upper, dtype=np.uint8)
#         mask = cv2.inRange(image_hsv, lower, upper)
#         mask_total = cv2.bitwise_or(mask_total, mask)

#     # ใช้ Mask ในการดึงเฉพาะสีที่ต้องการ
#     return cv2.bitwise_and(image, image, mask=mask_total)

# # รันกระบวนการกรองสีสองครั้ง
# filtered_image = filter_colors(image)
# filtered_image = filter_colors(filtered_image)

# # แสดงภาพที่ผ่านการกรอง
# plt.figure(figsize=(6, 6))
# plt.imshow(cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB))
# plt.title("Filtered Image")
# plt.axis("off")
# plt.show()

# # บันทึกผลลัพธ์
# output_filtered_path = "filtered_image.png"
# cv2.imwrite(output_filtered_path, filtered_image)

# print(f"ดาวน์โหลดภาพที่ผ่านการกรองได้ที่: {output_filtered_path}")


