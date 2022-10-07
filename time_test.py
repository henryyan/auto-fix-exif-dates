import datetime

al = 1588259702226


def convertTimeFromMills(ms):
    a = datetime.datetime.fromtimestamp(ms / 1000.0)
    print("{}".format(a)[0:19])


convertTimeFromMills(al)