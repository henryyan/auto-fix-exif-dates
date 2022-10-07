import filedate

# https://improveandrepeat.com/2022/04/python-friday-120-modify-the-create-date-of-a-file/

a = "D:\\huawei\\tmp\\1586923494543.mp4"
# a = "D:\\huawei\\wenwen-photo-huawei\\2020.4\\VID_20200424_165459.mp4"
a_file = filedate.File(a)

a_file.set(
    created="2022:01:01 13:00:00",
    modified="2022:01:01 14:00:00",
    accessed="2022:01:01 15:00:00"
)

after = filedate.File(a)
print(after.get())
