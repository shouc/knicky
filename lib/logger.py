# -*- coding:utf-8 -*-

class log(object):
    WARNING_COLOR = '\033[1;37m' 
    ERROR_COLOR   = '\033[1;31m'
    INFO_COLOR    = '\033[1;34m'
    PASS_COLOR    = '\033[1;32m'
    END_COLOR = '\033[0m'
    @staticmethod
    def logError(msg):
        print("[Error]: %s%s%s"%(log.ERROR_COLOR, msg, log.END_COLOR))

    @staticmethod
    def logWarn(msg):
        print("[Warning]: %s%s%s"%(log.WARNING_COLOR, msg, log.END_COLOR))

    @staticmethod
    def logInfo(msg):
        print("[Info]: %s%s%s"%(log.INFO_COLOR, msg, log.END_COLOR))

    @staticmethod
    def logPass(msg):
        print("[Pass]: %s%s%s"%(log.PASS_COLOR, msg, log.END_COLOR))

    @staticmethod
    def logTable(msg):
        print("%s%s%s"%(log.PASS_COLOR, msg, log.END_COLOR))
