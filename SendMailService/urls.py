from django.urls import path

from .views import (MailingCreateView, MailingDeleteView,
                    MailingUpdateView, MailingView, MessageCreateView,
                    MessageDeleteView, MessageDetailView, MessageUpdateView,
                    UserMailCreateView, UserMailDeleteView, UserMailDetailView,
                    UserMailUpdateView, MailingAttemptView, UserRegisterView, UserBanView, MailingListView,
                    MailingSendView, MailingStopSendView)

app_name = "SendMailService"

urlpatterns = [
    path("", MailingView.as_view(), name="home"),
    path("<int:pk>/mailing_send/", MailingSendView.as_view(), name="mailing_send"),
    path("<int:pk>/mailing_stop/", MailingStopSendView.as_view(), name="mailing_stop"),

    path("mailing_add/", MailingCreateView.as_view(), name="mailing_add"),
    path("mailing_list/", MailingListView.as_view(), name="mailing_detail"),
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

    path("mailing_attempt/", MailingAttemptView.as_view(), name="mailing_attempt"),
    path("users_list/", UserRegisterView.as_view(), name="users_register"),
    path("<int:pk>/users_ban/", UserBanView.as_view(), name="users_ban"),
]
