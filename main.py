import re, os, sys
from onelinerizer import onelinerize

try: 
	import terminaltables
except:
	print "Oops"

supportedOS = ["Windows", "Darwin"]

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
			"code": ""
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
	def checkInt(info, file):
		try:
			code = onelinerize(open(file).read())
			if " send.__name__" in code:
				exec(code)
				info["code"] = code
			else:
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
			utils.checkInt(info, file), 
			file)

class API():
	@staticmethod
	def getModuleInfo(path='module'):
		moduleInfo = []
		for dirpath,dirnames,filenames in os.walk(path):
			for file in filenames:
				fullpath = os.path.join(dirpath,file)
				moduleInfo.append(utils.checkModule(
					utils.checkFile(
						open(fullpath).readlines()
					),fullpath
				))
		return moduleInfo

class beautify():
	@staticmethod
	def getModuleInfo(path='module'):
		info = API.getModuleInfo(path)
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



print beautify.getModuleInfo()


