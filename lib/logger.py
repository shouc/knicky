# -*- coding:utf-8 -*-

class log(object):

    WARRING_COLOR = '\033[1;37m'  # yellow
    ERROR_COLOR   = '\033[1;31m'  # red
    INFO_COLOR    = '\033[1;34m'  # blue
    PASS_COLOR    = '\033[1;32m'  # green
    END_COLOR = '\033[0m'

    @staticmethod
    def logError(msg):
        print("[Error]: %s%s%s"%(log.ERROR_COLOR, msg, log.END_COLOR))
    
    @staticmethod
    def logWarn(msg):
        print("[Warning]: %s%s%s"%(log.WARRING_COLOR, msg, log.END_COLOR))

    @staticmethod
    def logInfo(msg):
        print("[Info]: %s%s%s"%(log.INFO_COLOR, msg, log.END_COLOR))

    @staticmethod
    def logPass(msg):
        print("[Pass]: %s%s%s"%(log.PASS_COLOR, msg, log.END_COLOR))

    @staticmethod
    def logTable(msg):
        print("%s%s%s"%(log.PASS_COLOR, msg, log.END_COLOR))
