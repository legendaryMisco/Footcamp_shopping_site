from email.message import EmailMessage
import ssl
import smtplib
from django.db.models.signals import post_save
from .models import Product,Subscription


def createProdcut(sender,instance,created,**kwargs):
    if created:
        product=instance
        subscribers = Subscription.objects.all().values_list('email')

        email_sender = 'akinolabahubali@gmail.com'
        email_password = 'stfsiwgsyozphcid'
        email_receiver = subscribers

        subject = "FOOTCAMP"
        body = f"""
        NEW PRODUCT "{product.product_title}" WAS JUST UPLOADED
        FOOT CAMP 
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

post_save.connect(createProdcut,sender=Product)