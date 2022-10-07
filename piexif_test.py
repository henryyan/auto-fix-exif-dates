import piexif

#path = r'D:\huawei\tmp\mmexport1590448439994.jpg'
from PIL import Image

path = r'D:\huawei\tmp\IMG_20200411_105746.jpg'
new_exif = {}
try:
    exif_dict = piexif.load(path)
    print(exif_dict['Exif'])
    print("aaa: {}".format(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]))
    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: u"2020-04-30 23:15:02",
        piexif.ExifIFD.DateTimeDigitized: u"2020-04-30 23:15:02"
    }
    new_exif = exif_ifd
except Exception as err:
    print("err: {}".format(err))
    # 1. cover1588259702226.png
    ms = 0


# new_exif = adjust_exif(exif_dict)
exif_dict = {"Exif": new_exif}
# print(exif_dict)
#exif_bytes = piexif.dump(exif_dict)
#piexif.insert(exif_bytes, path)
#im.save(path, "jpeg", exif=exif_bytes)