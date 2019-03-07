from django.core.mail import send_mail

def send_confirmation_mail():
    """Отправка письма для подтверждения email"""
    pass

def send_password_recovery_link(email, link):
    """Отправка письма со ссылкой на восстановление пароля"""
    
    email = "slamvsem@gmail.com"
    link = "http://digitalnsk.sibtiger.com/user/recovery-password?hash="+link
    send_mail(  subject = 'Подтверждение',
                message = link,
                from_email = 'sibtiger.nsk@gmail.com',
                recipient_list = [email],
                fail_silently=False)


