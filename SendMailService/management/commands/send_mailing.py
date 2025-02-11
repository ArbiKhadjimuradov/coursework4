import smtplib

from django.utils import timezone

from django.core.mail import send_mail
from django.core.management.base import BaseCommand

import os
from dotenv import load_dotenv

from SendMailService.models import Mailing, MailingAttempt

load_dotenv(override=True)


class Command(BaseCommand):
    def handle(self, *args, **options):

        for obj in Mailing.objects.filter(status='Создана'):
            try:
                email = [user_mail.email for user_mail in obj.user_mail.all()]

                obj.date_start = timezone.now()
                obj.status = 'Запущена'
                obj.save()

                server_response = send_mail(
                    subject=f'{obj.message.head_letter}',
                    message=f'{obj.message.body_letter}',
                    recipient_list=email,
                    fail_silently=False,
                    from_email=os.getenv('EMAIL_HOST_USER')
                )

                obj.date_end = timezone.now()
                obj.status = 'Завершена'
                obj.save()

                mailing_attempt = MailingAttempt.objects.create(mailing=obj, mail_response=server_response)
                if server_response:
                    mailing_attempt.status = 'Успешно'
                else:
                    mailing_attempt.status = 'Не успешно'
                mailing_attempt.save()

            except smtplib.SMTPException as error:
                MailingAttempt.objects.create(mailing=obj, mail_response=error, status='Не успешно')
