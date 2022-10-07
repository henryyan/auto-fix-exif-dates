# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import re
import time
from datetime import datetime
from pathlib import Path

import filedate
import piexif
from PIL import Image
from piexif import InvalidImageDataError


def cal_datetime(filename, fmt_str):
    # new_date = datetime(2018, 1, 1, 0, 0, 0).strftime("%Y:%m:%d %H:%M:%S")

    # IMG_20200410_161219
    # cover1588259702226
    print("path: {}".format(filename))

    # 匹配时间戳类型
    search_mills = re.findall("[0-9]{10}", filename)
    search_huawei_date = re.findall("[0-9]{8}_[0-9]{6}", filename)
    # print("a: {}, b: {}".format(search_mills, search_huawei_date))

    if len(search_huawei_date) > 0:
        aaa = search_huawei_date[0]
        # print("\t get new filename: {}".format(aaa))
        bbb = aaa.replace("IMG_", "")
        # print("\t get date str: {}".format(bbb))
        nd = time.strptime(bbb, "%Y%m%d_%H%M%S")
        # print("\t nd: {}".format(nd))
        new_date = datetime(nd.tm_year, nd.tm_mon, nd.tm_mday, nd.tm_hour, nd.tm_min, nd.tm_sec).strftime(fmt_str)
        # print("\t exif date from huawei: {}".format(new_date))

    if len(search_mills) > 0:
        new_date = datetime.fromtimestamp(int(search_mills[0])).strftime(fmt_str)
        # print("\t exif date from ts: {}".format(new_date))

    return new_date


# Press the green button in the gutter to run the script.
# 参考文档： https://stackoverflow.com/questions/33031663/how-to-change-image-captured-date-in-python
if __name__ == '__main__':
    photo_dir = "D:\\huawei\\wenwen-photo-huawei\\2020.4"
    for filename in os.listdir(photo_dir):
        file_path = os.path.join(photo_dir, filename)
        try:
            if not filename.endswith("jpg") and not filename.endswith("png") and not filename.endswith("mp4"):
                continue

            if filename.startswith(".VID"):
                continue

            # 替换png为jpg
            if filename.endswith("png"):
                im1 = Image.open(file_path)
                jpg_file_path = file_path.replace("png", "jpg")
                filename = filename.replace("png", "jpg")
                print("create new jpg file: {}".format(jpg_file_path))
                im1.save(jpg_file_path)
                print("saved new jpg file: {}".format(jpg_file_path))
                file_path = jpg_file_path
                # delete origin jpg

            # 文件三个日期属性
            mp4_datetime = cal_datetime(filename, "%Y-%m-%d %H:%M:%S")
            print("get mp4 date: {}".format(mp4_datetime))
            a_file = filedate.File(file_path)

            a_file.set(
                created=mp4_datetime,
                modified=mp4_datetime,
                accessed=mp4_datetime
            )

            # 写入exif到jpg文件
            paths = Path(file_path).stem
            print("fill exif for file: {}".format(file_path))

            if filename.endswith("jpg") or filename.endswith("jpeg"):
                new_exif = piexif.load(file_path)
                print("handle jpg file: {}".format(filename))
                # print("\t get exif: {}".format(new_exif))
                if not new_exif.__contains__(piexif.ExifIFD.DateTimeOriginal):
                    # new_exif = set_exif(new_exif)

                    new_date = cal_datetime(filename, "%Y:%m:%d %H:%M:%S")

                    new_exif['0th'][piexif.ImageIFD.DateTime] = new_date
                    new_exif['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
                    new_exif['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
                    # print("abc: {}".format(new_exif))
                    exif_bytes = piexif.dump(new_exif)
                    piexif.insert(exif_bytes, file_path)
        except InvalidImageDataError as err:
            print("get err: {}".format(err))
            continue
