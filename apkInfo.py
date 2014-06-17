import os,sys
import shutil
import string
import re

AAPT_PATH = 'aapt'

def getAppBaseInfo(apkpath):
    appBaseInfoDict = {'PkgName':None,'VersionCode':None,'VersionName':None,'AppLabel':None,'SdkVersion':None}
    try:
        aaptCmd = AAPT_PATH + ' d badging ' + apkpath
        cmdOut = os.popen(aaptCmd)
        outList = cmdOut.readlines()
        cmdOut.close()

        for line in outList:
            if line.find('package:') != -1:
                #print line
                item_list = line.split('''' ''')
                #print item_list
                for item in item_list:
                    item = item.rstrip('\n')
                    if item.find('name=') != -1:
                        content_list = item.split('name=')
                        if len(content_list) > 0:
                            appBaseInfoDict['PkgName'] = content_list[-1].strip("''")
                    elif item.find('versionCode=') != -1:
                        content_list = item.split('versionCode=')
                        if len(content_list) > 0:
                            appBaseInfoDict['VersionCode'] = content_list[-1].strip("''")
                    elif item.find('versionName=') != -1:
                        content_list = item.split('versionName=')
                        if len(content_list) > 0:
                            appBaseInfoDict['VersionName'] = content_list[-1].strip("''")
            elif line.find('application-label:') != -1:
                line = line.rstrip('\n')
                content_list = line.split('application-label:')
                if len(content_list) > 0:
                    appBaseInfoDict['AppLabel'] = content_list[-1].strip("''")
            elif line.find('sdkVersion:') != -1:
                line = line.rstrip('\n')
                content_list = line.split('sdkVersion:')
                if len(content_list) > 0:
                    appBaseInfoDict['SdkVersion'] = content_list[-1].strip("''")
        return appBaseInfoDict
    except:
        return appBaseInfoDict


def getCertInfo(apkpath):
    apkCert = {'MD5':None}
    javaPath = '''"'''
    try:
        certPath = javaPath + '''jar"''' + " tf "  + '' + apkpath
        #print(certPath)
        cmdOut = os.popen(certPath)
        outList = cmdOut.readlines()
        #print(outList)

        for line in outList:
            #print line
            if line.find('.RSA') != -1:
                extract = javaPath + '''jar"''' + " xf "  + apkpath + ' ' + line
                #print extract
                os.popen(extract)
                keytoolCmd = javaPath + '''keytool"''' + " -printcert -file " + line
                certInfo = os.popen(keytoolCmd).readlines()
                #print certInfo
                for md5 in certInfo:
                    if md5.find('MD5:') != -1:
                        md5 = md5.replace('MD5:', '').strip()
                        apkCert['MD5'] = md5
                shutil.rmtree("META-INF")

        #print outList
        cmdOut.close()
        return apkCert
    except:
        print "except ---------------------------------"
        return apkCert


def getVersionDict(bInfo):
    pattern=r'\d*\.\d*\.\d*\.\d*\(([A-Za-z][\S]+|[A-Za-z][\S]+\sPAL\d*\.\d*)\)'
    if not checkPattern(pattern, bInfo['VersionName']):
        return
    versionDict = {'allNum':None, 'UE':None, 'UE1':None, 'UE2':None, 'numOfMaster':None,
            'numOfOther':None, 'posOfLBracket':None, 'posOfRBracket':None, 'branch':None,
            'pal':None, 'attrsCount':None, 'strCountInBracket':None}
    vName = bInfo['VersionName']
    versionDict['posOfLBracket'] = vName.find('(')
    versionDict['posOfRBracket'] = vName.find(')')
    strInBracket = ''
    if versionDict['posOfLBracket'] != -1 and versionDict['posOfRBracket'] != -1:
        strInBracket = vName[versionDict['posOfLBracket']  + 1:versionDict['posOfRBracket']]
    bracketList = strInBracket.split(' ');
    versionDict['strCountInBracket'] = len(bracketList)

    if len(bracketList) == 1:
        versionDict['branch'] = bracketList[0]
    if len(bracketList) == 2:
        versionDict['branch'] = bracketList[0]
        versionDict['pal'] = bracketList[1]
    versionDict['attrsCount'] = vName.count(' ')

    if versionDict['posOfLBracket'] != -1:
        versionDict['allNum'] = vName[:versionDict['posOfLBracket']]

        vNumList = versionDict['allNum'].split('.')
        versionDict['UE1'] = vNumList[0]
        versionDict['UE2'] = vNumList[1]
        versionDict['UE'] = vNumList[0] + '.' + vNumList[1]
        versionDict['numOfMaster'] = vNumList[2]
        versionDict['numOfOther'] = vNumList[3]
    #print versionDict
    return versionDict


def getFileNameDict(fileName):
    pattern=r'^[A-Z][A-Za-z0-9]+_\d*\.\d*\.\d*\.\d*-([A-Za-z][\S]+|[A-Za-z][\S]+-PAL\d*\.\d*)\.apk'
    if not checkPattern(pattern, bInfo['VersionName']):
        return

    fileDict = {'fullName':None, 'baseName':None,'extName':None,'allNum':None, 'UE':None, 'UE1':None,
            'UE2':None, 'numOfMaster':None, 'numOfOther':None, 'posOfUl':None, 'posOfMl':None, 'posOfExtName':None,
            'posOfPal':None, 'branch':None, 'pal':None, 'attrsCount':None}
    fileDict['fullName'] = fileName
    fileDict['extName'] = '.apk'
    fileDict['posOfUl'] = fileName.find('_')
    fileDict['posOfExtName'] = fileName.find('.apk')
    fileDict['baseName'] = fileName[:fileDict['posOfExtName']]
    fileDict['posOfMl'] = fileName.find('-')
    fileDict['allNum'] = fileName[fileDict['posOfUl'] + 1:fileDict['posOfMl']]
    fileDict = fileDict['allNum'].split('.')
    fileDict['UE1'] = allNumList[0]
    fileDict['UE2'] = allNumList[1]
    fileDict['numOfMaster'] = allNumList[2]
    fileDict['numOfOther'] = allNumList[3]
    fileDict['UE'] = allNumList[0] + '.' + allNumList[1]

    attrs = fileName[fileDict['posOfMl'] + 1:fileDict['posOfExtName']]
    attrsCount = 0
    fileDict['posOfPal'] = attrs.upper().find('PAL')

    if ileDict['posOfPal'] == -1:
        attrsCount = 1
        fileDict['branch'] = fileName[fileDict['posOfMl'] + 1:fileDict['posOfExtName'] - 1]
        print ileDict['branch']
    else:
        attrsCount = 2
        fileDict['branch'] = fileName[fileDict['posOfMl'] + 1:fileDict['posOfPal'] - 1]
        fileDict['pal'] = fileName[fileDict['posOfPal'] + 1:fileDict['posOfExtName']]
        print fileDict['branch']
        print fileDict['pal']
    fileDict['attrsCount'] = attrsCount

    #attrsCount = fileName.count('-')
    #fileDict['attrsCount'] = attrsCount
    #print attrsCount
    #if attrsCount == 1:
        #fileDict['branch'] = attrsList[0]
    #elif attrsCount == 2:
        #fileDict['branch'] = attrsList[0]
        #fileDict['pal'] = attrsList[1]
    #print fileDict
    return fileDict


def isAccord(fileName, versionName):
    v1 = versionName.replace('(', '-')
    v2 = v1.replace(' ', '-')
    v3 = v2.replace(')', '')
    if fileName.find(v3) == -1:
        #print(fileName + ' is not accordance with ' + versionName)
        return False
    else:
        return True


def checkPattern(pattern, s):
    if re.match(pattern,s):
        #print pattern,'matches',s
        return True
    else:
        print('match failed: ' + pattern + ' does not matches ' + s)
        return False


def checkCert(cInfo):
    keyDict = {'cbb':'C6:EC:D6:5C:CB:DE:0B:54:A9:45:42:3C:8A:F8:20:19', 'platform':'8D:DB:34:2F:2D:A5:40:84:02:D7:56:8A:F2:1E:29:F9',
               'testKey':'E8:9B:15:8E:4B:CF:98:8E:BD:09:EB:83:F5:37:8E:87', 'media':'19:00:BB:FB:A7:56:ED:D3:41:90:22:57:6F:38:14:FF',
               'shared':'5D:C8:20:1F:7D:B1:BA:4B:9C:8F:C4:41:46:C5:BC:C2'}
    md5 = cInfo['MD5']
    for key,value in keyDict.iteritems():
        #print value
        if value == md5:
            #print 'Keystore: ' + key
            return key
    #print('Keystore: Unknown')
    return None



def checkRules(apkName):
    #print(apkName)
    pattern=r'^[A-Z][A-Za-z0-9]+_\d*\.\d*\.\d*\.\d*-([A-Za-z][\S]+|[A-Za-z][\S]+-PAL\d*\.\d*)\.apk'
    if not checkPattern(pattern, os.path.basename(apkName)):
        return False

    bInfo = getAppBaseInfo(apkName)
    cInfo = getCertInfo(apkName)
    vInfo = getVersionDict(bInfo)

    #print('MD5: ' + cInfo['MD5'])
    key = checkCert(cInfo)
    if key == None:
        print('Keystore: Unknown')
    else:
        print 'Keystore: ' + key

    print('version name: ' + bInfo['VersionName'])
    if not isAccord(os.path.basename(apkName), bInfo['VersionName']):
        print(os.path.basename(apkName) + ' is not accordance with ' + bInfo['VersionName'])
        return False

    if vInfo['branch'] == 'normal' and string.atoi(vInfo['numOfOther']) != 0:
        print('version_name: The master branch version number must be 0')
        return False
    if vInfo['branch'] != 'normal' and string.atoi(vInfo['numOfOther']) == 0:
        print('version_name: The other branch version number must not be 0')
        return False
    return True



def diff(apk1, apk2):
    if os.path.splitext(apk1)[1].lower() != '.apk' or os.path.splitext(apk2)[1].lower() != '.apk':
        print('Not apk files')
        return

    bInfo1 = getAppBaseInfo(apk1)
    #print(bInfo1)
    vInfo1 = getVersionDict(bInfo1)
    cInfo1 = getCertInfo(apk1)
    #print cInfo1

    bInfo2 = getAppBaseInfo(apk2)
    vInfo2 = getVersionDict(bInfo2)
    cInfo2 = getCertInfo(apk2)

    result = True

    if bInfo1 == None or cInfo1 == None or vInfo1 == None or bInfo2 == None or cInfo2 == None or vInfo2 == None:
        print('\nFAILED: ' + apk1 + ' Can not update to ' + apk2)
        return

    b1 = isAccord(apk1, bInfo1['VersionName'])
    if not b1:
        print('WARNING: Old apk ' + apk1 + ' is not accordance with ' + bInfo1['VersionName'])
        #pass
        #return
    #print(bInfo2)
    b2 = isAccord(apk2, bInfo2['VersionName'])
    if not b2:
        print('FAILED: new apk ' + apk2 + ' is not accordance with ' + bInfo2['VersionName'])
        print('FAILED: ' + apk1 + ' Can not update to ' + apk2)
        return

    print('Package Name: ' + bInfo1['PkgName'] + ' --> ' + bInfo2['PkgName'])
    if not (bInfo1['PkgName'] == bInfo2['PkgName']):
        result = False
        print('Package Name: failed\n')
    else:
        print('Package Name: succeed\n')

    print('VersionCode: ' + bInfo1['VersionCode'] + ' --> ' + bInfo2['VersionCode'])
    if not string.atoi(bInfo1['VersionCode']) < string.atoi(bInfo2['VersionCode']):
        result = False
        print('VersionCode: failed\n')
    else:
        print('VersionCode: succeed\n')

    key1 = checkCert(cInfo1)
    key2 = checkCert(cInfo2)
    print('Keystore: ' + key1 + ' --> ' + key2)
    if key1 != None and key2 != None and key1 == key2:
        print('Keystore: succeed\n')
    else:
        result = False
        print('Keystore: failed\n')

    print('VersionName: ' + bInfo1['VersionName'] + ' --> ' + bInfo2['VersionName'] + '\n')

    print(' UE: ' + vInfo1['UE'] + ' --> ' + vInfo2['UE'])
    if string.atoi(vInfo1['UE1']) > string.atoi(vInfo2['UE1']):
        result = False
        print(' UE: failed\n')
    elif (vInfo1['UE1'] == vInfo2['UE1']) and (string.atoi(vInfo1['UE2']) > string.atoi(vInfo2['UE2'])):
        result = False
        print(' UE: failed\n')
    else:
        print(' UE: succeed\n')

    print(' branch: ' + vInfo1['branch'] + ' --> ' + vInfo2['branch'])
    print(' master(normal) branch number: ' + vInfo1['numOfMaster'] + ' --> ' + vInfo2['numOfMaster'])
    print(' other branch number: ' + vInfo1['numOfOther'] + ' --> ' + vInfo2['numOfOther'])
    if vInfo1['branch'] == 'normal' and vInfo2['branch'] == 'normal':
        if not string.atoi(vInfo1['numOfMaster']) < string.atoi(vInfo2['numOfMaster']):
            result = False
            print(' branch number: failed')
        elif string.atoi(vInfo1['numOfOther']) == 0 and string.atoi(vInfo2['numOfOther']) == 0:
            print(' branch number: succeed')
        else:
            result = False
            print(' branch number: failed')
    elif vInfo1['branch'] == vInfo2['branch']:
        if vInfo1(['numOfMaster']) <= vInfo2(['numOfMaster']) and vInfo1(['numOfOther']) <= vInfo2(['numOfOther']):
            print(' branch number: succeed')
        else:
            result = False
            print(' branch number: failed')
    else:
        result = False
        print(' branch number: failed')
    if result:
        print('\nSUCCEED: ' + apk1 + ' Can update to ' + apk2)
    else:
        print('\nFAILED: ' + apk1 + ' Can not update to ' + apk2)


if __name__ == "__main__":
    pass
