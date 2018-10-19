__sys__ = ["Windows", "Darwin", "Linux"];
__name__ = "userInfo"
__desc__ = "Get User Info"

def send():
	import os
	return os.popen("whoami").read().replace('\n', '') 