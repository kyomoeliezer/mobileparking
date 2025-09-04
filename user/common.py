from django.conf import settings
######################################
from django.core.mail import send_mail,EmailMessage

def send_Mmail(to,subject,msg):
        email = EmailMessage(
        subject=subject,
        body=msg,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to],
        reply_to=[settings.DEFAULT_FROM_EMAIL],
        headers={'Message-ID': 'ABD'},
        )
        email.content_subtype = "html"
        return email.send(fail_silently=False)





def send_Email(idOb,email_list,subject,message):
    from django.core.mail import EmailMessage, get_connection
    from django.core.mail import send_mail
    from django.conf import settings
    try:

        import mimetypes
        import random

        email_from = settings.DEFAULT_FROM_EMAIL
        headers = {'Message-ID': str(idOb)},
        email = EmailMessage(subject, message, email_from, email_list, reply_to=email_from)

        email.send()

        return 1
    except Exception as e:
        return e


