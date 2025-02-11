import os

from django.core.mail import send_mail
from django.utils import timezone
from dotenv import load_dotenv
from django.core.cache import cache

from config.settings import CACHE_ENABLED
from SendMailService.models import MailingAttempt, Mailing

load_dotenv(override=True)


class FormValid:
    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user

        mailing.save()
        return super().form_valid(form)


def send_mailing(self):
    """Функция отправки сообщений по рассылке"""
    email = [user_mail.email for user_mail in self.object.user_mail.all()]

    self.object.date_start = timezone.now()
    self.object.status = 'Запущена'
    self.object.save()

    server_response = send_mail(
        subject=f'{self.object.message.head_letter}',
        message=f'{self.object.message.body_letter}',
        recipient_list=email,
        fail_silently=False,
        from_email=os.getenv('EMAIL_HOST_USER')
    )

    self.object.date_end = timezone.now()
    self.object.status = 'Завершена'
    self.object.save()

    mailing_attempt = MailingAttempt.objects.create(mailing=self.object, mail_response=server_response,
                                                    owner=self.request.user)
    if server_response:
        mailing_attempt.status = 'Успешно'
    else:
        mailing_attempt.status = 'Не успешно'
    mailing_attempt.save()


class GetListMailing:
    """Класс обработки получения списка продуктов"""
    @staticmethod
    def get_list_mailing_from_cache():
        """Метод получает данные от БД, если списка продуктов нет в кэше, то добавляет его и возвращает список"""
        if not CACHE_ENABLED:
            return Mailing.objects.all()
        key = 'mailing_list'
        mailing = cache.get(key)

        if mailing is not None:
            return mailing
        products = Mailing.objects.all()
        cache.set(key, products)
        return products
