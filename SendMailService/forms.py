from django.forms import ModelForm


from .models import Mailing, UserMail, Message


class MailingForm(ModelForm):
    """Класс создания формы добавления рассылки"""

    class Meta:
        model = Mailing
        exclude = (
            "date_start",
            "date_end",
            "status",
            "owner",
        )

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields["message"].widget.attrs.update(
            {"class": "form-select", "placeholder": "Выберите сообщение"}
        )
        self.fields["user_mail"].widget.attrs.update(
            {"class": "form-select", "placeholder": "Выберите получателей"}
        )


class UserMailForm(ModelForm):
    """Класс создания формы добавления получателя рассылки"""

    class Meta:
        model = UserMail
        exclude = ("owner",)


def __init__(self, *args, **kwargs):
    super(UserMailForm, self).__init__(*args, **kwargs)

    self.fields["email"].widget.attrs.update(
        {"class": "form-control", "placeholder": "Введите email получателя"}
    )
    self.fields["fullname"].widget.attrs.update(
        {"class": "form-control", "placeholder": "Введите ФИО получателя"}
    )
    self.fields["comment"].widget.attrs.update(
        {"class": "form-control", "placeholder": "Дополнительная информация"}
    )


def clean(self):
    """Валидация данных сообщения (не должны иметь запрещенные слова)"""
    cleaned_data = super().clean()
    email = cleaned_data.get("email")
    fullname = cleaned_data.get("fullname")
    comment = cleaned_data.get("comment")
    banned_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    for word in banned_words:
        if word in email.lower():
            self.add_error(
                "email",
                f'Нельзя использовать слово "{word.title()}" в почтовом адресе.',
            )
        if word in fullname.lower():
            self.add_error(
                "fullname", f'Нельзя использовать слово "{word.title()}" в ФИО.'
            )
        if word in comment.lower():
            self.add_error(
                "comment",
                f'Нельзя использовать слово "{word.title()}" в подробной информации.',
            )


class MessageForm(ModelForm):
    """Класс создания формы добавления письма"""

    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["head_letter"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите тему письма"}
        )
        self.fields["body_letter"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите письмо"}
        )

    def clean(self):
        """Валидация данных сообщения (не должны иметь запрещенные слова)"""
        cleaned_data = super().clean()
        head_letter = cleaned_data.get("head_letter")
        body_letter = cleaned_data.get("body_letter")
        banned_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]

        for word in banned_words:
            if word in head_letter.lower():
                self.add_error(
                    "head_letter",
                    f'Нельзя использовать слово "{word.title()}" в теме письма.',
                )
            if word in body_letter.lower():
                self.add_error(
                    "body_letter",
                    f'Нельзя использовать слово "{word.title()}" в содержании письма.',
                )
