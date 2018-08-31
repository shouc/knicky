__sys__ = "*";
__name__ = "Sendgrid"
__desc__ = "Use sendgrid"


def send(_content, _module):
    import time, os, email, json, string, base64
    import sendgrid
    import getpass
    from sendgrid.helpers.mail import Email, Mail, Content
    from random import randint
    _content = str(_content)
    _module = str(_module)
    
    apiKey = "CHANGE HERE"
    toEmailAdd = "CHANGE HERE"
    
    sg = sendgrid.SendGridAPIClient(apikey = apiKey)
    fromEmail = Email("knicky@knicky-test.com")
    toEmail = Email(toEmailAdd)
    subject = "%s 's test" % randint(0, 20000)
    content = Content("text/plain", "@msgstart@%s@msgend@" % {
        "_content": base64.b64encode(_content),
        "_id": "%s" % str(time.time()) + str(randint(0, 100)),
        "_date": str(time.time()),
        "_from": getpass.getuser(),
        "_byModule": _module
    })
    mail = Mail(fromEmail, subject, toEmail, content)
    response = sg.client.mail.send.post(request_body=mail.get())


def receive(_range, _page):
    import time, os, email, json, string, base64
    import poplib
    
    _server = "CHANGE HERE"   
    _user = "CHANGE HERE"
    _password = "CHANGE HERE"
    
    server = poplib.POP3_SSL(_server)
    server.user(_user)
    server.pass_(_password)
    resp, items, octets = server.list()
    _range = _range if len(items) > _range else len(items)
    _page = _page if len(items) / _range > _page else len(items) / _range
    result = []
    for m in range(_range * (_page - 1), _range * _page):
        id, size = string.split(items[m])
        resp, text, octets = server.retr(id)
        content = ""
        for i in text:
            if "_from" in i:
                pass
            if "=" in i[-1:]:
                content += i.replace("=","")
            else:
                content += i
        result.append(json.loads(content.split("@msgstart@")[1]\
            .split("@msgend@")[0].replace("'", '"')))
    
    return result
