from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def signup_email(username, receiver):
    # Creating message subject and sender
    subject = 'Welcome KEJU'
    sender = settings.EMAIL_HOST_USER

    #passing in the context vairables
    text_content = render_to_string('email/signup.txt',{"username": username})
    html_content = render_to_string('email/signup.html',{"username": username})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()