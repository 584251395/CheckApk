import sys
import os
import apkInfo


def printInfo(filePath):
    ext = os.path.splitext(filePath)[1]
    if ext.lower() == '.apk':
        print(filePath)
        if apkInfo.checkRules(filePath):
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

    for path, dirs, files in os.walk(startdir):
        for f in files:
            pf = path + os.sep + f
            if not os.path.isdir(pf):
                printInfo(pf)


def main(argv):
    apkInfo.AAPT_PATH = os.getcwd() + os.sep + 'aapt'
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
