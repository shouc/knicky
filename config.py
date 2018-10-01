import core
import lib.sha1Info
from core import updateBase
class sgUpdate(updateBase):
    def __init__(self, _user="None",
        _password="None", _server="None", 
        _apiKey="None", bypass=False):
        self.user = _user
        self.password =_password
        self.server = _server
        self.apiKey = _apiKey
        self.bypass = bypass
        self.updateList = [
            {"original":"user", "after":_user, "desc":"The Email Address"},
            {"original":"password", "after":_password, "desc":"The Password of that Email Address"},
            {"original":"server", "after":_server, "desc":"The POP Server of the Email Address"},
            {"original":"apiKey", "after":_apiKey, "desc":"The API key of the Sendgrid"},
        ]
    def main(self):
        try:
            temp = open("messenger/sg.uninit").read()
            if not self.bypass:
                if core.utils.getSHA1(temp) == lib.sha1Info.sg:
                    core.utils.updateFile("messenger/sg.uninit",
                        self.updateList)
                    return "Success"
                else:
                    return ("[!] Error! Template file (%s) is not correct"
                        % core.utils.getSHA1(temp))
            core.utils.updateFile("messenger/sg.uninit",
                        self.updateList)
            return "Success"
        except:
            return "[!] Error! No template file found"

class qcloudUpdate(updateBase):
    def __init__(self,  _secretID="None",
        _secretKey="None", _region="None", 
        _bucket="None", bypass=False):
        self.secretID = _secretID
        self.secretKey = _secretKey
        self.region = _region
        self.bucket = _bucket
        self.bypass = bypass
        self.updateList = [
            {"original":"secretID", "after":_secretID, "desc":"Secret ID for API"},
            {"original":"secretKey", "after":_secretKey, "desc":"Secret ket for API"},
            {"original":"region", "after":_region, "desc":"Region of the bucket"},
            {"original":"bucket", "after":_bucket, "desc":"Name of the bucket"},
        ]
    def main(self):
        try:
            temp = open("messenger/qcloud.uninit").read()
            if not self.bypass:
                if core.utils.getSHA1(temp) == lib.sha1Info.qcloud:
                    core.utils.updateFile("messenger/qcloud.uninit",
                        self.updateList)
                    return "Success"
                else:
                    return ("[!] Error! Template file (%s) is not correct"
                        % core.utils.getSHA1(temp))
            core.utils.updateFile("messenger/qcloud.uninit",
                        self.updateList)
            return "Success"
        except:
            return "[!] Error! No template file found"
