import requests
import json


def send_email(subject, to_email, html):

    url = 'https://api.sendinblue.com/v3/smtp/email'

    headers = {'Content-Type': 'application/json',
               'api-key': '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'}

    payload = {"tags": ["user_initiated_email"],
               "sender": {"name": "cs691", "email": "support@cs691.com"},
               "to": [{"email": to_email}],
               "replyTo": {"email": "support@cs691.com", "name": "cs691"},
               "subject": subject,
               "htmlContent": html
               }

    payload = json.dumps(payload)

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == requests.codes.created:
        return
    else:
        print(response.status_code)
        print(response.content)
        print(response.text)


