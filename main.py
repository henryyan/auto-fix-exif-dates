# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
from datetime import datetime
from pathlib import Path
import piexif
from PIL import Image
from piexif import InvalidImageDataError


def set_exif(origin_exif):
    """

    :param origin_exif:
    :return:
    """
    exif_ifd = {}
    if origin_exif is not None:
        exif_ifd = origin_exif

    new_date = "2020-04-30 23:15:02"
    exif_ifd['0th'][piexif.ImageIFD.DateTime] = new_date
    exif_ifd['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
    exif_ifd['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
    return exif_ifd


def cal_datetime(filename):
    new_date = datetime(2018, 1, 1, 0, 0, 0).strftime("%Y:%m:%d %H:%M:%S")

    # IMG_20200410_161219
    # cover1588259702226
    print("path: {}".format(filename))


    return new_date


# Press the green button in the gutter to run the script.
# 参考文档： https://stackoverflow.com/questions/33031663/how-to-change-image-captured-date-in-python
if __name__ == '__main__':
    photo_dir = "D:\\huawei\\tmp"
    for filename in os.listdir(photo_dir):
        file_path = os.path.join(photo_dir, filename)
        try:
            if not filename.endswith("jpg") and not filename.endswith("png"):
                continue

            # 替换png为jpg
            if filename.endswith("png"):
                im1 = Image.open(file_path)
                jpg_file_path = file_path.replace("png", "jpg")
                print("create new jpg file: {}".format(jpg_file_path))
                im1.save(jpg_file_path)
                print("saved new jpg file: {}".format(jpg_file_path))
                file_path = jpg_file_path
                # delete origin jpg

            paths = Path(file_path).stem
            print("fill exit for file: {}".format(file_path))

            new_exif = piexif.load(file_path)
            # print("\t get exif: {}".format(new_exif))
            if not new_exif.__contains__(piexif.ExifIFD.DateTimeOriginal):
                # new_exif = set_exif(new_exif)

                new_date = cal_datetime(filename)

                new_exif['0th'][piexif.ImageIFD.DateTime] = new_date
                new_exif['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
                new_exif['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
                # print("abc: {}".format(new_exif))
                exif_bytes = piexif.dump(new_exif)
                piexif.insert(exif_bytes, file_path)

                #print("\t replace exif with: {}".format(new_exif))
                #exif_bytes = piexif.dump(new_exif)
                #piexif.insert(exif_bytes, file_path)
        except InvalidImageDataError as err:
            print("get err: {}".format(err))
            # print("no exif: {}".format(file_path))
            # new_exif = set_exif(None)
            # print("get new exif: {}".format(new_exif))
            # print("final exif info: {}".format(new_exif))
            # exif_bytes = piexif.dump(new_exif)
            # piexif.insert(exif_bytes, file_path)
