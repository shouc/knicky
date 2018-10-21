#-*- coding:utf-8 -*-

import core, config
import argparse
from lib.logger import log
from lib.msg import *

#Importing libs
import time, random, ast
class utils():
    @staticmethod
    def getClassName():
        classNames = []
        for i in ast.walk(ast.parse(open("config.py").read())):
            try:
                if isinstance(i, ast.ClassDef):
                    classNames.append(i.name)
            except:
                pass
        return classNames

def configUpdate(args):
    executeCode = "obj = config.%s(" % (args.n)
    for i in args.param:
        exec("val = args.%s" % i)
        executeCode += "%s='%s', " % (i, val)
    executeCode += "bypass=%s)" % (args.bypass)
    exec("result = %s" % executeCode) 
    print(result.main())

def getModuleInfo(args):
    log.logTable(core.beautify.getModuleInfo())

def getSendInfo(args):
    log.logTable(core.beautify.getSendInfo())

def createProj(args):
    if not args.platform:
        log.logWarn(platformWarn)
        platform = "Darwin"
    else:
        platform = args.platform
    if not args.name:
        log.logWarn(nameWarn)
        name = str(core.utils.base64Encode(str(time.time() + 
            random.randint(0,20000)))).replace("=", "")
    else:
        name = args.name
    print(
        core.API.createProj(
            moduleList=[i for i in args.moduleList.split("+")], 
            sendList=[i for i in args.sendList.split("+")], 
            platform=platform,
            projName=name,
            sendPath='messenger',
            modulePath="module"
        )
    )

def listProj(args):
    log.logTable(core.beautify.listProj())

def receiveInfo(args):
    if not args.range:
        log.logWarn(rangeWarn)
        _range = 10
    else:
        _range = args.range
    log.logTable(
        core.beautify.receiveInfo(
            projName=args.name,
            _range=_range
        )
    )

def main():
    parser = argparse.ArgumentParser(description=descOfCLI)
    subparsers = parser.add_subparsers(help='commands')

    #getModuleInfo
    getModuleInfoParser = subparsers.add_parser('getModuleInfo', 
        help=descOfGetModuleInfo)
    getModuleInfoParser.set_defaults(func=getModuleInfo)

    #getSendInfo
    getSendInfoParser = subparsers.add_parser('getSendInfo', 
        help=descOfGetSendInfo)
    getSendInfoParser.set_defaults(func=getSendInfo)

    #createVirus
    createProjParser = subparsers.add_parser('createProj', 
        help=descOfCreateProj)
    createProjParser.add_argument("moduleList", help=descOfModuleList)
    createProjParser.add_argument("sendList", help=descOfSendList)
    createProjParser.add_argument("-p", "--platform", help=descOfPlatform,
        choices=['Darwin','Windows','Linux'])
    createProjParser.add_argument("-n", "--name", help=descOfProjName)
    createProjParser.set_defaults(func=createProj)

    #listProj
    listProjParser = subparsers.add_parser('listProj', 
        help=descOfListProj)
    listProjParser.set_defaults(func=listProj)

    #receiveInfo
    receiveInfoParser = subparsers.add_parser('receiveInfo', 
        help=descOfReceiveInfo)
    receiveInfoParser.add_argument("name", help=descOfProjName)
    receiveInfoParser.add_argument("-r", "--range", help=descOfRange,
        type=int)
    receiveInfoParser.set_defaults(func=receiveInfo)

    #config
    for i in utils.getClassName():
        exec("configObj = config.%s()" % i)
        exec("config%sParser = subparsers.add_parser('%s', help=descOfConfig)" % \
            (i, i))
        for j in configObj.getU():
            exec("config%sParser.add_argument('--%s', help='%s', required=True)" % \
                (i, j['original'], j['desc']))
        exec("""config%sParser.add_argument('-b', '--bypass', help='%s',
            default=False)""" % \
            (i, descOfBypass))
        exec("""config%sParser.set_defaults(func=configUpdate, n='%s', 
                param=%s)""" % \
            (i, i, [x["original"] for x in configObj.getU()]))

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
