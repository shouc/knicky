import core
import lib.sha1Info

def sgUpdate(showInfo=False, _user="None",
    _password="None", _server="None", 
    _apiKey="None", bypass=False):
    updateList = [
        {"original":"user", "after":_user, "desc":"The Email Address"},
        {"original":"password", "after":_password, "desc":"The Password of that Email Address"},
        {"original":"server", "after":_server, "desc":"The POP Server of the Email Address"},
        {"original":"apiKey", "after":_apiKey, "desc":"The API key of the Sendgrid"},
    ]
    if showInfo:
        return core.beautify.showInfo(updateList)
    try:
        temp = open("messenger/sg.uninit").read()
        if not bypass:
            if core.utils.getSHA1(temp) == lib.sha1Info.sg:
                core.utils.updateFile("messenger/sg.uninit",
                    updateList)
                return "Success"
            else:
                return ("[!] Error! Template file (%s) is not correct"
                    % core.utils.getSHA1(temp))
        core.utils.updateFile("messenger/sg.uninit",
                    updateList)
        return "Success"
    except:
        return "[!] Error! No template file found"

def qcloudUpdate(showInfo=False, _secretID="None",
    _secretKey="None", _region="None", 
    _bucket="None", bypass=False):
    updateList = [
        {"original":"secretID", "after":_secretID, "desc":"Secret ID for API"},
        {"original":"secretKey", "after":_secretKey, "desc":"Secret ket for API"},
        {"original":"region", "after":_region, "desc":"Region of the bucket"},
        {"original":"bucket", "after":_bucket, "desc":"Name of the bucket"},
    ]
    if showInfo:
        return core.beautify.showInfo(updateList)
    
    temp = open("messenger/qcloud.uninit").read()
    if not bypass:
        if core.utils.getSHA1(temp) == lib.sha1Info.qcloud:
            core.utils.updateFile("messenger/qcloud.uninit",
                updateList)
            return "Success"
        else:
            return ("[!] Error! Template file (%s) is not correct"
                % core.utils.getSHA1(temp))
    core.utils.updateFile("messenger/qcloud.uninit",
                updateList)
    return "Success"
