import core
import lib.sha1Info

def sgUpdate(showInfo=False, _user="None",
    _password="None", _server="None", 
    _apiKey="None"):
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
        if core.utils.getSHA1(temp) == lib.sha1Info.sg:
            core.utils.updateFile("messenger/sg.uninit",
                updateList)
        else:
            return ("[!] Error! Template file (%s) is not correct"
                % core.utils.getSHA1(temp))
    except:
        return "[!] Error! No template file found"
