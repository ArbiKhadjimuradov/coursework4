# from django.http import HttpResponse
# from django.shortcuts import render

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

        return context


class MailingCreateView(CreateView):
    """Класс представления создания рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_add.html"
    context_object_name = "mailing_add"

    form_class = MailingForm
    success_url = reverse_lazy("SendMailService:home")


class MailingDetailView(DetailView):
    """Класс представления детальной рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_detail.html"
    context_object_name = "mailing_detail"


class MailingUpdateView(UpdateView):
    """Класс представления обновления рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_add.html"
    context_object_name = "mailing_update"

    form_class = MailingForm

    def get_success_url(self):
        return reverse("SendMailService:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(DeleteView):
    """Класс представления удаления рассылки"""

    model = Mailing
    template_name = "SendMailService/mailing_delete.html"
    context_object_name = "mailing_delete"

    success_url = reverse_lazy("SendMailService:home")


class UserMailDetailView(DetailView):
    """Класс представления всех получателей рассылки"""

    template_name = "SendMailService/user_detail.html"
    context_object_name = "user_detail"


class UserMailCreateView(CreateView):
    """Класс представления создания получателей рассылки"""

    model = UserMail
    template_name = "SendMailService/user_create.html"
    context_object_name = "user_create"

    form_class = UserMailForm
    success_url = reverse_lazy("SendMailService:home")


class UserMailUpdateView(UpdateView):
    """Класс представления обновления получателей рассылки"""

    model = UserMail
    template_name = "SendMailService/user_create.html"
    context_object_name = "user_update"

    form_class = UserMailForm

    def get_success_url(self):
        return reverse("SendMailService:user_detail", args=[self.kwargs.get("pk")])


class UserMailDeleteView(DeleteView):
    """Класс представления удаления получателей рассылки"""

    model = UserMail
    template_name = "SendMailService/user_delete.html"
    context_object_name = "user_delete"

    success_url = reverse_lazy("SendMailService:home")


class MessageDetailView(DetailView):
    """Класс представления писем"""

    model = Message
    template_name = "SendMailService/message_detail.html"
    context_object_name = "message_detail"


class MessageCreateView(CreateView):
    """Класс представления создания писем"""

    model = Message
    template_name = "SendMailService/message_create.html"
    context_object_name = "message_create"

    form_class = MessageForm
    success_url = reverse_lazy("SendMailService:home")


class MessageUpdateView(UpdateView):
    """Класс представления обновления писем"""

    model = Message
    template_name = "SendMailService/message_create.html"
    context_object_name = "message_update"

    form_class = MessageForm

    def get_success_url(self):
        return reverse("SendMailService:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(DeleteView):
    """Класс представления удаления писем"""

    model = Message
    template_name = "SendMailService/message_confirm_delete.html"
    context_object_name = "message_delete"

    success_url = reverse_lazy("SendMailService:home")


class MailingAttemptView(ListView):
    """Класс представления Всех рассылок на главной странице"""

    model = MailingAttempt
    template_name = "SendMailService/home.html"
    context_object_name = "mailing_attempt"
