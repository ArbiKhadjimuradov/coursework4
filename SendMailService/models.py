from django.db import models


# Create your models here.
class UserMail(models.Model):
    """Модель создания получателя рассылки"""
    objects = None

    email = models.CharField(unique=True, max_length=150, verbose_name='Email', null=False,
                             blank=False)  # столбцы таблицы
    fullname = models.CharField(max_length=250, verbose_name='Ф.И.О.', null=False, blank=False)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f"{self.fullname}"

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['email', 'fullname']


class Message(models.Model):
    """Модель создания сообщения"""
    objects = None

    head_letter = models.CharField(max_length=300, verbose_name='Тема_письма')
    body_letter = models.TextField(verbose_name='Тело_письма')

    def __str__(self):
        return f"{self.head_letter}: тема письма"

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ['head_letter', 'body_letter']


class Mailing(models.Model):
    """Модель создания рассылки"""
    objects = None

    date_start = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки")
    date_end = models.DateTimeField(auto_now=True, verbose_name="Время окончания отправки")
    status = models.CharField(max_length=9, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='messages')
    user_mail = models.ManyToManyField(UserMail, related_name='users')

    def __str__(self):
        return f"Рассылка в статусе: {self.status}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['date_start', 'date_end', 'status', 'message']


class MailingAttempt(models.Model):
    """Модель создания попытки рассылки"""
    datetime_attempt = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки рассылки")
    status = models.CharField(max_length=10, verbose_name="Статус")
    mail_response = models.TextField(verbose_name="Ответ почтового сервиса")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_attempts')

    def __str__(self):
        return f"Попытка рассылки: {self.status}"

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['datetime_attempt', 'status', 'mail_response', 'mailing']