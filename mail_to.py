import smtplib
import ssl
from email.message import EmailMessage

from password_generator import em_password


def mail_supplier(product, quantity):
    email_sender = 'example@mail.com'
    email_password = em_password

    email_receiver = ''
    # email_receiver = email
    subject = 'subject'
    body = 'body'

    em = EmailMessage()
    em['From'] = email_sender
    em['TO'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return "Sent"
