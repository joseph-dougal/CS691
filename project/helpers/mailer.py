from flask_mail import Mail, Message


def sendmail(subject, sender, recipient, body):
    try:
        msg = Message(subject, sender=sender, recipients=[recipient])
        msg.body = body
        print(body)
        # mail.send(msg)
        return "Sent"
    except Exception as e:
        return e
