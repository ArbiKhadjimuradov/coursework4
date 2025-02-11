import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_start",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Время отправки"
                    ),
                ),
                (
                    "date_end",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Время окончания отправки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Создана", "Создана"),
                            ("Запущена", "Запущена"),
                            ("Завершена", "Завершена"),
                        ],
                        default="Создана",
                        max_length=9,
                        verbose_name="Статус",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
                "ordering": ["date_start", "date_end", "status", "message"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "head_letter",
                    models.CharField(max_length=300, verbose_name="Тема_письма"),
                ),
                ("body_letter", models.TextField(verbose_name="Тело_письма")),
            ],
            options={
                "verbose_name": "Письмо",
                "verbose_name_plural": "Письма",
                "ordering": ["head_letter", "body_letter"],
            },
        ),
        migrations.CreateModel(
            name="UserMail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.CharField(max_length=150, unique=True, verbose_name="Email"),
                ),
                ("fullname", models.CharField(max_length=250, verbose_name="Ф.И.О.")),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="Комментарий"),
                ),
            ],
            options={
                "verbose_name": "Получатель",
                "verbose_name_plural": "Получатели",
                "ordering": ["email", "fullname"],
            },
        ),
        migrations.CreateModel(
            name="MailingAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "datetime_attempt",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время попытки рассылки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Success", "Успешно"),
                            ("Not successful", "Не успешно"),
                        ],
                        max_length=14,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "mail_response",
                    models.TextField(verbose_name="Ответ почтового сервиса"),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mailing_attempts",
                        to="SendMailService.mailing",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылки",
                "ordering": ["datetime_attempt", "status", "mail_response", "mailing"],
            },
        ),
        migrations.AddField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="SendMailService.message",
                verbose_name="Письмо",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="user_mail",
            field=models.ManyToManyField(
                related_name="users",
                to="SendMailService.usermail",
                verbose_name="Получатели",
            ),
        ),
    ]
