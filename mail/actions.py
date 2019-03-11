from django.core.mail import send_mail
import after_response


from bs4 import BeautifulSoup
import string


def send_confirmation_mail():
    """Отправка письма для подтверждения email"""
    pass

@after_response.enable
def send_password_recovery_link(email, link):
    """Отправка письма со ссылкой на восстановление пароля"""

    link = "http://digitalnsk.sibtiger.com/recovery/?hash="+link
    #email = "slamvsem@gmail.com" #it's temp line

    f = open('/home/dato/Рабочий стол/Digital/DigitalNSK/mail/static/mail/recovery.html', 'r')
    html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    a = soup.find(id = "root")
    a["href"] = link
    htmlMsg = str(soup)
    send_mail(  subject = 'Подтверждение',
                message = ' ',
                html_message= htmlMsg,
                from_email = 'sibtiger.nsk@gmail.com',
                recipient_list = [email],
                fail_silently=False)


