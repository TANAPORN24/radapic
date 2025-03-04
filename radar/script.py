import os
from PIL import Image
import numpy as np

# Input file path
input_path = "input/skn240_HQ_latest.gif"  # เปลี่ยนเป็นไฟล์ที่ต้องการใช้

# Extract file name without extension
file_name = os.path.basename(input_path)  # เช่น "skn240_HQ_latest (2).gif"
file_name_no_ext, file_ext = os.path.splitext(file_name)  # แยกชื่อไฟล์และนามสกุล

# Define output path
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี
output_path = os.path.join(output_folder, f"{file_name_no_ext}.png")  # เปลี่ยนเป็น PNG

# Load the radar image (GIF format)
image = Image.open(input_path).convert("RGBA")

# Convert image to numpy array
image_data = np.array(image)

# Define a mask to preserve only the radar data (excluding the map background but keeping the scale)
def is_rain_data(pixel):
    r, g, b, a = pixel
    return not (40 < r < 180 and 60 < g < 200 and 40 < b < 180)  # กรองสีที่เป็นพื้นหลัง

# Apply mask to remove background
mask = np.apply_along_axis(is_rain_data, -1, image_data)
image_data[~mask] = [0, 0, 0, 0]  # Make non-rain areas transparent

# Remove blue and white colors
blue_lower = np.array([0, 0, 100, 0])  # Lower bound for blue (RGBA)
blue_upper = np.array([100, 255, 255, 255])  # Upper bound for blue (RGBA)
white_lower = np.array([200, 200, 200, 0])  # Lower bound for white (RGBA)
white_upper = np.array([255, 255, 255, 255])  # Upper bound for white (RGBA)

blue_mask = ((image_data[:, :, 0] >= blue_lower[0]) & (image_data[:, :, 0] <= blue_upper[0]) &
             (image_data[:, :, 1] >= blue_lower[1]) & (image_data[:, :, 1] <= blue_upper[1]) &
             (image_data[:, :, 2] >= blue_lower[2]) & (image_data[:, :, 2] <= blue_upper[2]))

white_mask = ((image_data[:, :, 0] >= white_lower[0]) & (image_data[:, :, 0] <= white_upper[0]) &
              (image_data[:, :, 1] >= white_lower[1]) & (image_data[:, :, 1] <= white_upper[1]) &
              (image_data[:, :, 2] >= white_lower[2]) & (image_data[:, :, 2] <= white_upper[2]))

final_mask = blue_mask | white_mask
image_data[final_mask] = [0, 0, 0, 0]  # Make detected colors transparent

# Convert back to image
processed_image = Image.fromarray(image_data)

# Crop image to defined size (1745x1585 pixels, aligned to top-right)
crop_width = 1745
crop_height = 1585
orig_width, orig_height = processed_image.size
left = orig_width - crop_width  # Align to right
upper = 0  # Align to top
right = orig_width
lower = crop_height
cropped_rain_image = processed_image.crop((left, upper, right, lower))

# Apply Circular Crop
width, height = cropped_rain_image.size
center_x, center_y = width // 2, height // 2
radius = 792

# Create a circular mask
mask = Image.new("L", (width, height), 0)
mask_data = np.array(mask)
y, x = np.ogrid[:height, :width]
mask_area = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
mask_data[mask_area] = 255
circular_mask = Image.fromarray(mask_data, mode="L")

# Apply circular mask to the cropped image
circular_rain_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
circular_rain_image.paste(cropped_rain_image, (0, 0), circular_mask)

# Save the final circular cropped image
circular_rain_image.save(output_path)

print(f"Saved final image: {output_path}")
