import os
import smtplib
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from users.models import CustomUser
from SendMailService.models import UserMail, Mailing, Message, MailingAttempt
from django.urls import reverse_lazy, reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from dotenv import load_dotenv
from SendMailService.forms import MailingForm, UserMailForm, MessageForm
from SendMailService.services import send_mailing, GetListMailing

load_dotenv(override=True)


class MailingView(ListView):
    """Класс представления Всех рассылок на главной странице"""

    model = Mailing
    template_name = "SendMailService/home.html"
    context_object_name = "mailing"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_mail"] = UserMail.objects.all()
        context["mailing_all_started"] = Mailing.objects.filter(status="Запущена")
        if self.request.user.is_authenticated:
            context['user_usermail'] = UserMail.objects.filter(owner=self.request.user)
            context['user_mailing_started'] = Mailing.objects.filter(owner=self.request.user, status='Запущена')
            context['user_mailing'] = Mailing.objects.filter(owner=self.request.user)

        return context

    def get_queryset(self):
        """Настройка серверного кэширования главной страницы"""
        return GetListMailing.get_list_mailing_from_cache()


class MailingStopSendView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "SendMailService/mailing_stop.html"
    context_object_name = "mailing_stop"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.has_perm("can_stop_mailing"):
            self.object.status = "Отключена"
            self.object.save()
        return self.object


class MailingSendView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "SendMailService/mailing_send.html"
    context_object_name = "mailing_send"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        if self.object.owner == self.request.user and self.object.status == "Создана":
            try:
                send_mailing(self)  # Функция в разделе сервисы, отправляет сообщения по рассылке
            except smtplib.SMTPException as error:
                MailingAttempt.objects.create(mailing=self.object, mail_response=error, status='Не успешно')
        return self.object


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Класс представления создания рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_add.html"
    context_object_name = "mailing_add"

    form_class = MailingForm
    success_url = reverse_lazy("SendMailService:mailing_detail")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user

        mailing.save()
        return super().form_valid(form)


@method_decorator(cache_page(60), name='dispatch')
class MailingListView(LoginRequiredMixin, ListView):
    """Класс представления детальной рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_detail.html"
    context_object_name = "mailing_detail"

    def get_queryset(self):
        user = self.request.user

        if user.has_perm('SendMailService.can_view_mailing'):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления обновления рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_add.html"
    context_object_name = "mailing_update"

    form_class = MailingForm

    def get_success_url(self):
        return reverse("SendMailService:mailing_detail")

    def get_form_class(self):
        """
        Проверка чтобы пользователь был владельцем продукта и тогда может его изменять
        и если у пользовтаеля есть право can_unpublish_product
        """
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления удаления рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_delete.html"
    context_object_name = "mailing_delete"

    success_url = reverse_lazy("SendMailService:mailing_detail")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return super().get_form_class()
        raise PermissionDenied


@method_decorator(cache_page(60), name='dispatch')
class UserMailDetailView(LoginRequiredMixin, ListView):
    """Класс представления всех получателей рассылки"""

    template_name = "SendMailService/user_detail.html"
    context_object_name = "user_detail"

    def get_queryset(self):
        user = self.request.user

        if user.has_perm('SendMailService.can_view_user_mail'):
            return UserMail.objects.all()
        return UserMail.objects.filter(owner=user)


class UserMailCreateView(LoginRequiredMixin, CreateView):
    """Класс представления создания получателей рассылки"""

    model = UserMail
    template_name = "SendMailService/user_create.html"
    context_object_name = "user_create"

    form_class = UserMailForm
    success_url = reverse_lazy("SendMailService:user_mail_detail")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()

        return super().form_valid(form)


class UserMailUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления обновления получателей рассылки"""

    model = UserMail
    template_name = "SendMailService/user_create.html"
    context_object_name = "user_update"

    form_class = UserMailForm

    def get_success_url(self):
        return reverse("SendMailService:user_mail_detail")

    def get_form_class(self):
        """
        Проверка чтобы пользователь был владельцем продукта и тогда может его изменять
        и если у пользовтаеля есть право can_unpublish_product
        """
        user = self.request.user
        if user == self.object.owner:
            return UserMailForm
        raise PermissionDenied


class UserMailDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления удаления получателей рассылки"""

    model = UserMail
    template_name = "SendMailService/user_delete.html"
    context_object_name = "user_delete"

    success_url = reverse_lazy("SendMailService:user_mail_detail")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return super().get_form_class()
        raise PermissionDenied


@method_decorator(cache_page(60), name='dispatch')
class MessageDetailView(LoginRequiredMixin, ListView):
    """Класс представления писем"""

    model = Message
    template_name = "SendMailService/message_detail.html"
    context_object_name = "message_detail"

    def get_queryset(self):
        user = self.request.user

        if user.has_perm('SendMailService.can_view_message'):
            return Message.objects.all()
        return Message.objects.filter(owner=user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Класс представления создания писем"""

    model = Message
    template_name = "SendMailService/message_create.html"
    context_object_name = "message_create"

    form_class = MessageForm
    success_url = reverse_lazy("SendMailService:message_detail")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Класс представления обновления писем"""

    model = Message
    template_name = "SendMailService/message_create.html"
    context_object_name = "message_update"

    form_class = MessageForm

    def get_success_url(self):
        return reverse("SendMailService:message_detail")

    def get_form_class(self):
        """
        Проверка чтобы пользователь был владельцем продукта и тогда может его изменять
        и если у пользовтаеля есть право can_unpublish_product
        """
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Класс представления удаления писем"""

    model = Message
    template_name = "SendMailService/message_confirm_delete.html"
    context_object_name = "message_delete"

    success_url = reverse_lazy("SendMailService:home")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return super().get_form_class()
        raise PermissionDenied


@method_decorator(cache_page(60), name='dispatch')
class MailingAttemptView(LoginRequiredMixin, ListView):
    """Класс представления Всех рассылок на главной странице"""

    model = MailingAttempt
    template_name = "SendMailService/mailing_attempt_detail.html"
    context_object_name = "mailing_attempt"

    def get_queryset(self):
        return MailingAttempt.objects.filter(owner=self.request.user)


class UserRegisterView(LoginRequiredMixin, ListView):
    """Класс представления Всех рассылок на главной странице"""

    model = CustomUser
    template_name = "SendMailService/user_register_view.html"
    context_object_name = "users"

    def get_queryset(self):
        user = self.request.user

        if user.has_perm('users.can_ban_user'):
            return CustomUser.objects.all()
        return PermissionDenied


class UserBanView(LoginRequiredMixin, DeleteView):
    """Класс представления блокировки пользователей"""

    model = CustomUser
    template_name = "SendMailService/user_register_ban.html"
    context_object_name = "user_ban"
    success_url = reverse_lazy("SendMailService:users_register")

    def get_queryset(self):
        user = self.request.user

        if user.has_perm('users.can_ban_user'):
            return CustomUser.objects.all()
        return PermissionDenied

    def form_valid(self, form):
        success_url = self.get_success_url()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(success_url)
