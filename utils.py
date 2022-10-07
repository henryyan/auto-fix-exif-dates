import re
import time
from datetime import datetime


def cal_datetime(filename, fmt_str, default_year, default_month):
    new_date = ""

    # IMG_20200410_161219
    # cover1588259702226
    # print("path: {}".format(filename))

    # 匹配时间戳类型
    search_mills = re.findall("(1[5-6][0-9]{8})", filename)

    # 20200506_190807
    search_huawei_date = re.findall("202[0-9]{5}_[0-9]{6}", filename)
    # print("a: {}, b: {}".format(search_mills, search_huawei_date))

    if len(search_huawei_date) > 0:
        aaa = search_huawei_date[0]
        # print("\t get date str: {}".format(bbb))
        nd = time.strptime(aaa, "%Y%m%d_%H%M%S")
        # print("\t nd: {}".format(nd))
        new_date = datetime(nd.tm_year, nd.tm_mon, nd.tm_mday, nd.tm_hour, nd.tm_min, nd.tm_sec).strftime(fmt_str)
        # print("\t exif date from huawei: {}".format(new_date))

    if len(search_mills) > 0 and len(new_date) == 0:
        new_date = datetime.fromtimestamp(int(search_mills[0])).strftime(fmt_str)
        # print("\t exif date from ts: {}".format(new_date))

    if len(new_date) == 0:
        new_date = datetime(default_year, default_month, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")

    print("\tget final date: {} for file； {}".format(new_date, filename))
    return new_date

if __name__ == '__main__':
    s = cal_datetime("mmexport1593824020216_103170904150.mp4", "%Y-%m-%d %H:%M:%S")
    print(s)
