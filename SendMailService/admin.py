from .models import UserMail, Message, Mailing, MailingAttempt
from django.contrib import admin


@admin.register(UserMail)
class UserMailAdmin(admin.ModelAdmin):
    """Отображает модели получателей рассылки в админке"""

    list_display = (
        "id",
        "email",
        "fullname",
        "comment",
    )
    list_filter = (
        "email",
        "fullname",
    )
    search_fields = ("id", "email", "fullname")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Отображает модели письма в админке"""

    list_display = (
        "id",
        "head_letter",
        "body_letter",
    )
    list_filter = (
        "id",
        "head_letter",
    )
    search_fields = (
        "id",
        "head_letter",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Отображает модели рассылки в админке"""

    list_display = (
        "id",
        "date_start",
        "date_end",
        "status",
        "message",
    )
    list_filter = (
        "id",
        "date_start",
        "date_end",
        "status",
        "message",
        "user_mail",
    )
    search_fields = (
        "id",
        "date_start",
        "date_end",
        "status",
        "message",
        "user_mail",
    )


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    """Отображает модели попытки рассылки в админке"""

    list_display = (
        "id",
        "datetime_attempt",
        "status",
        "mail_response",
        "mailing",
    )
    list_filter = (
        "id",
        "datetime_attempt",
        "status",
        "mail_response",
        "mailing",
    )
    search_fields = (
        "id",
        "datetime_attempt",
        "status",
        "mail_response",
        "mailing",
    )
