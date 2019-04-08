from django.core.mail import send_mail
import after_response

from DigitalNSK import settings

from bs4 import BeautifulSoup
import string

@after_response.enable
def send_confirmation_mail(email, link):
    """Отправка письма для подтверждения email"""

    link = "http://digitalnsk.ru/?hash="+link

    f = open(f'{settings.STATIC_ROOT}/mail/confirm_registration.html', 'r')
    html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    a = soup.find(id = "root")
    a["href"] = link
    htmlMsg = str(soup)
    send_mail(  subject = 'Подтверждение аккаунта',
                message = ' ',
                html_message= htmlMsg,
                from_email = 'sibtiger.nsk@gmail.com',
                recipient_list = [email],
                fail_silently=False)
    

@after_response.enable
def send_password_recovery_link(email, link):
    """Отправка письма со ссылкой на восстановление пароля"""

    link = "http://digitalnsk.ru/recovery/?hash="+link
    #email = "slamvsem@gmail.com" #it's temp line

    f = open(f'{settings.STATIC_ROOT}/mail/recovery.html', 'r')
    html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    a = soup.find(id = "root")
    a["href"] = link
    htmlMsg = str(soup)
    send_mail(  subject = 'Восстаноление пароля',
                message = ' ',
                html_message= htmlMsg,
                from_email = 'sibtiger.nsk@gmail.com',
                recipient_list = [email],
                fail_silently=False)


