from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from email.message import EmailMessage
import ssl
import smtplib
from django.conf import  settings
from django.db.models.signals import post_save,post_delete
from .models import Register


def createAccount(sender,instance,created,**kwargs):
    if created:
        user=instance
        customer = Register.objects.create(
            user=user,
            username=user.username,
            name=user.first_name,
            email=user.email
        )

        email_sender = 'akinolabahubali@gmail.com'
        email_password = 'stfsiwgsyozphcid'
        email_receiver = customer.email

        subject = "FOOTCAMP"
        body = """
        thank you for joining footcamp
        """
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


def updateAccount(sender,instance,created,**kwargs):
    customer = instance
    user = customer.user
    if created == False:
        user = customer.user
        user.username = customer.username
        user.first_name = customer.name
        user.email = customer.email
        user.save()


def deleteAccount(sender,instance,**kwargs):
    user = instance.user
    user.delete()

post_save.connect(createAccount,sender=User)
post_save.connect(updateAccount,sender=Register)
post_delete.connect(deleteAccount,sender=Register)