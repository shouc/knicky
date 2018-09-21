__sys__ = ["Darwin", "Linux"];
__name__ = "wifiInfo"
__desc__ = "Get ifconfig"



def send():
	import os
	import re
	return os.popen("ifconfig").read()

