import urllib.request
import urllib.parse

def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return (fr)

resp = sendSMS('3S8wQWP88SU-nORP14zJiJMnZ9ljDpYhIObXZUbQEI', '9462540078',
               '', 'This is your demo message, send from python')
print(resp)