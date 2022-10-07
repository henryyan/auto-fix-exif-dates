import io

import PIL.Image
from PIL import Image

img = PIL.Image.open('D:\\huawei\\photo\\2020.4\\IMG_20200410_161219.jpg')
# img = PIL.Image.open('D:\\huawei\\tmp\\cover1588259702226.png')
exif_data = img.getexif()
print("exif data:{}".format(exif_data))

# EXIF CODES: https://exiv2.org/tags.html
# 拍摄日期代码：306
create_datetime = exif_data[306]
print(create_datetime)

# Make memory buffer for JPEG-encoded image
buffer = io.BytesIO()

# Convert OpenCV image onto PIL Image
OpenCVImageAsPIL = Image.fromarray(img)

# Encode newly-created image into memory as JPEG along with EXIF from other image
OpenCVImageAsPIL.save(buffer, format='JPEG', exif=exif_data.info['exif'])
