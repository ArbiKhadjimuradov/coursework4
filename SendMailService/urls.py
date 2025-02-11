from django.urls import path

from .views import (MailingView, MailingDetailView, MailingUpdateView, MailingDeleteView, MailingCreateView,
                    UserMailCreateView, UserMailDetailView, UserMailUpdateView,
                    UserMailDeleteView, MessageCreateView, MessageDetailView, MessageUpdateView,
                    MessageDeleteView,)

app_name = "SendMailService"

urlpatterns = [
    path("", MailingView.as_view(), name="home"),

    path("mailing_add/", MailingCreateView.as_view(), name="mailing_add"),
    path("mailing_list/", MailingDetailView.as_view(), name="mailing_detail"),
    path("<int:pk>/update_mailing/", MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete_mailing/", MailingDeleteView.as_view(), name="mailing_delete"),

    path("user_mail_create/", UserMailCreateView.as_view(), name="user_mail_create"),
    path("user_mail_list/", UserMailDetailView.as_view(), name="user_mail_detail"),
    path("<int:pk>/update_user/", UserMailUpdateView.as_view(), name="user_mail_update"),
    path("<int:pk>/delete_user/", UserMailDeleteView.as_view(), name="user_mail_delete"),

    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path("message_list/", MessageDetailView.as_view(), name="message_detail"),
    path("<int:pk>/update_message/", MessageUpdateView.as_view(), name="message_update"),
    path("<int:pk>/delete_message/", MessageDeleteView.as_view(), name="message_delete"),
]
