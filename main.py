# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
from pathlib import Path

import filedate
import piexif
from PIL import Image
from piexif import InvalidImageDataError

from utils import cal_datetime

_default_year = 2015
_default_month = 12

# Press the green button in the gutter to run the script.
# 参考文档： https://stackoverflow.com/questions/33031663/how-to-change-image-captured-date-in-python
if __name__ == '__main__':
    photo_dir = "D:\\zhaopian\\{}.{}".format(_default_year, _default_month)
    for filename in os.listdir(photo_dir):
        file_path = os.path.join(photo_dir, filename)
        print("handling file: {} ...".format(file_path))
        try:
            filename = filename.lower()
            if not filename.endswith("jpg") and not filename.endswith("png") and not filename.endswith("mp4"):
                print("\tinvalid filename: {}".format(filename))
                continue

            if filename.startswith(".vid"):
                continue

            # remove repeat files
            if filename.__contains__("(1)"):
                temp_file_path = file_path.replace("(1)", "")
                if os.path.isfile(temp_file_path):
                    print("\t Remove repeat file: {}".format(file_path))
                    os.remove(file_path)
                    continue

            # 替换png为jpg
            png_filepath = ""
            if filename.endswith("png"):
                png_filepath = file_path
                im1 = Image.open(file_path)
                jpg_file_path = file_path.replace("png", "jpg")
                filename = filename.replace("png", "jpg")
                print("\tcreate new jpg file: {}".format(jpg_file_path))
                try:
                    im1.save(jpg_file_path)
                    print("\t1-saved new jpg file: {}".format(jpg_file_path))
                except:
                    # print("convert png to jpg, catch a error: {}".format(err))
                    im1 = im1.convert("RGB")
                    im1.save(jpg_file_path)
                    print("\t2-saved new jpg file: {}".format(jpg_file_path))
                file_path = jpg_file_path

            # 文件三个日期属性
            create_time = cal_datetime(filename, "%Y-%m-%d %H:%M:%S", _default_year, _default_month)
            create_time_v2 = create_time.replace("-", ":")
            a_file = filedate.File(file_path)

            a_file.set(
                created=create_time,
                modified=create_time,
                accessed=create_time
            )

            # 写入exif到jpg文件
            paths = Path(file_path).stem

            if filename.endswith("jpg") or filename.endswith("jpeg"):
                try:
                    new_exif = piexif.load(file_path)
                except:
                    print("\tfailed read exif info: {}".format(file_path))
                    continue

                print("\thandle jpg file: {}".format(filename))
                # print("\t get exif: {}".format(new_exif))
                # print("\t get date: {}".format(new_exif["{}".format(piexif.ExifIFD.DateTimeOriginal)]))
                # print("\t get date: {}".format(new_exif["Exif"].__contains__(piexif.ExifIFD.DateTimeOriginal)))
                if not new_exif.__contains__(piexif.ExifIFD.DateTimeOriginal) and not new_exif["Exif"].__contains__(piexif.ExifIFD.DateTimeOriginal):
                    # new_exif = set_exif(new_exif)
                    new_exif['0th'][piexif.ImageIFD.DateTime] = create_time_v2
                    new_exif['Exif'][piexif.ExifIFD.DateTimeOriginal] = create_time_v2
                    new_exif['Exif'][piexif.ExifIFD.DateTimeDigitized] = create_time_v2
                    print("abc: {}".format(new_exif))
                    # "dump" got wrong type of exif value.\n41729 in Exif IFD. Got as <class \'int\'>.
                    # See bug https://github.com/hMatoba/Piexif/issues/95
                    try:
                        del new_exif['Exif'][piexif.ExifIFD.SceneType]
                    except:
                        pass
                    try:
                        exif_bytes = piexif.dump(new_exif)
                        piexif.insert(exif_bytes, file_path)
                    except:
                        print("\t failed to dump exif: {}", file_path)
                        continue

            # remove png files
            if len(png_filepath) > 0:
                print("\tremove png file: {}".format(png_filepath))
                os.remove(png_filepath)


        except InvalidImageDataError as err:
            print("get err: {}".format(err))
            continue
