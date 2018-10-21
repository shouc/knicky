__sys__ = ["Windows", "Darwin", "Linux"];
__name__ = "alertHacked"
__desc__ = "Show a dialog with 'Hacked' on screen"

def send():
    import os, platform
    if platform.system() == "Darwin":
        try:
            os.popen('''osascript -e 'display dialog "Hacked"';''')
            return "Alerted"
        except:
            return "Failed"
    elif platform.system() == "Windows":
        try:
            os.popen('''mshta vbscript:msgbox("Hacked")(window.close)''')
            return "Alerted"
        except:
            return "Failed"
    elif platform.system() == "Linux":
        try:
            os.popen('''notify-send "Hacked";''')
            return "Alerted"
        except:
            return "Failed"
    else:
        return "Failed"
