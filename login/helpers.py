from django.core.mail import send_mail
import random

def send_forget_password_mail(email, code):
    subject = 'Your forget password code'
    message = f'Your forget password code: {code}'
    email_from = "fitlife.yazlab@gmail.com"
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


