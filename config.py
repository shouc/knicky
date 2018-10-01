import core
import lib.sha1Info
from core import updateBase
class sgUpdate(updateBase):
    def __init__(self, user="None",
        password="None", server="None", 
        apiKey="None", bypass=False):
        updateBase.__init__(self)
        self.user = user
        self.password = password
        self.server = server
        self.apiKey = apiKey
        self.bypass = bypass
        self.fileName = "messenger/sg.uninit"
        self.updateList = [
            {"original":"user", "after":user, "desc":"The Email Address"},
            {"original":"password", "after":password, "desc":"The Password of that Email Address"},
            {"original":"server", "after":server, "desc":"The POP Server of the Email Address"},
            {"original":"apiKey", "after":apiKey, "desc":"The API key of the Sendgrid"},
        ]
    

class qcloudUpdate(updateBase):
    def __init__(self,  secretID="None",
        secretKey="None", region="None", 
        bucket="None", bypass=False):
        updateBase.__init__(self)
        self.secretID = secretID
        self.secretKey = secretKey
        updateBase.stop(self)
        self.region = region
        self.bucket = bucket
        self.bypass = bypass
        self.fileName = "messenger/qcloud.uninit"
        self.updateList = [
            {"original":"secretID", "after":secretID, "desc":"Secret ID for API"},
            {"original":"secretKey", "after":secretKey, "desc":"Secret ket for API"},
            {"original":"region", "after":region, "desc":"Region of the bucket"},
            {"original":"bucket", "after":bucket, "desc":"Name of the bucket"},
        ]
