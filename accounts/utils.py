from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
def detectUser(user):
    if user.role==1:
        redirectUrl='vendordashboard'
        return redirectUrl
    elif user.role==2:
        redirectUrl='custdashboard'
        return redirectUrl
    elif user.role==None and user.is_superadmin:
        redirectUrl='/admin'
        return redirectUrl
    
def send_verification_email(request,user,mail_subject,email_template):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site=get_current_site(request)
    mail_subject='Please Activate Your Account'
    message=render_to_string(email_template,{
        'user':user,
        'domain':current_site,
        'uid':  urlsafe_base64_encode(force_bytes(user.pk)),    #this line is for encoding user's primary key
        'token':default_token_generator.make_token(user),  #make token will take user ani token generate karnaar
    })    
    to_email=user.email
    mail=EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.content_subtype="html"
    mail.send()

def send_notification(mail_subject,mail_template,context):
    from_email=settings.DEFAULT_FROM_EMAIL
    message=render_to_string(mail_template,context)
    if(isinstance(context['to_email'],str)):    #str madhe mail check kartoy
        to_email=[]
        to_email.append(context['to_email'])
    else:
        to_email=context['to_email']
    
    mail=EmailMessage(mail_subject,message,from_email,to=to_email)
    mail.content_subtype="html"
    mail.send()



