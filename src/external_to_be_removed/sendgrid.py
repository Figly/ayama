import requests

url = "https://api.sendgrid.com/v3/mail/send"

payload = '''{"personalizations": 
                [{"to": [{"email": "karel@lulalend.co.za"}]}],
                "from": {"email": "karelrverhoeven@gmail.com"},
                "subject": "Awe",
                "content": [{"type": "text/plain", "value": "Test email"}]}'''
headers = {
  'Authorization': 'Bearer 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', #just a test token, can do 100 emails per month 
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)
