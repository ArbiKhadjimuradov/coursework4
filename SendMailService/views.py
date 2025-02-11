from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from SendMailService.models import UserMail, Mailing, Message, MailingAttempt
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)
from SendMailService.forms import MailingForm, UserMailForm, MessageForm


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
            context['user_message'] = Message.objects.filter(owner=self.request.user)
            context['user_mailing_started'] = Mailing.objects.filter(owner=self.request.user, status='Запущена')
            context['user_mailing'] = Mailing.objects.filter(owner=self.request.user)
            context['user_mailingattempt'] = MailingAttempt.objects.filter(owner=self.request.user)

        return context


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


class MailingDetailView(LoginRequiredMixin, ListView):
    """Класс представления детальной рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_detail.html"
    context_object_name = "mailing_detail"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['mailing_owner_user'] = Mailing.objects.filter(owner=self.request.user)

        return context


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


class UserMailDetailView(LoginRequiredMixin, ListView):
    """Класс представления всех получателей рассылки"""

    template_name = "SendMailService/user_detail.html"
    context_object_name = "user_detail"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['user_mail_owner_user'] = UserMail.objects.filter(owner=self.request.user)

        return context


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


class MessageDetailView(LoginRequiredMixin, ListView):
    """Класс представления писем"""

    model = Message
    template_name = "SendMailService/message_detail.html"
    context_object_name = "message_detail"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['message_owner_user'] = Message.objects.filter(owner=self.request.user)

        return context


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


class MailingAttemptView(LoginRequiredMixin, ListView):
    """Класс представления Всех рассылок на главной странице"""

    model = MailingAttempt
    template_name = "SendMailService/home.html"
    context_object_name = "mailing_attempt"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user:
            return self.object
        raise PermissionDenied
