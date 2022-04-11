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


