import sys
import os
import apkInfo


def printInfo(filePath):
    ext = os.path.splitext(filePath)[1]
    if ext.lower() == '.apk':
        print(filePath)
        if apkInfo.checkRules(os.path.basename(filePath)):
            print("SUCCEED!!!")
        else:
            print('FAILED please check naming rules')
        print('\n')
    else:
        #print('Not apk files')
        pass


def scan(startdir):
    if not os.path.isdir(startdir):
        printInfo(startdir)
        return

    os.chdir(startdir)
    for obj in os.listdir(os.curdir):
        cwd = os.getcwd() + os.sep + obj
        printInfo(cwd)
        if os.path.isdir(obj):
            scan(obj)
            os.chdir(os.pardir)


def main(argv):
    if argv[1] == '-diff':
        apkInfo.diff(argv[2], argv[3])
        return
    if argv[1] == '-test':
        #getFileNameDict(argv[2])
        return
    for arg in argv[1:]:
        scan(arg)
if __name__ == '__main__':
    main(sys.argv)