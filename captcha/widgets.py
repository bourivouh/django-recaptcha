from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from captcha import client


class ReCaptcha(forms.widgets.Widget):
    nocaptcha_response_name = 'g-recaptcha-response'
    nocaptcha_challenge_name = 'g-recaptcha-response'
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def __init__(self, public_key=None, use_ssl=None, attrs={}, *args,
                 **kwargs):
        self.public_key = public_key if public_key else \
            settings.RECAPTCHA_PUBLIC_KEY
        self.use_ssl = use_ssl if use_ssl is not None else getattr(
            settings, 'RECAPTCHA_USE_SSL', False)
        self.js_attrs = attrs
        super(ReCaptcha, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % client.displayhtml(
            self.public_key,
            self.js_attrs, use_ssl=self.use_ssl))

    def value_from_datadict(self, data, files, name):
        if self.is_nocaptcha(data):
            challenge_name = self.nocaptcha_challenge_name
            response_name = self.nocaptcha_challenge_name
        else:
            challenge_name = self.recaptcha_challenge_name
            response_name = self.recaptcha_response_name

        return [
            data.get(challenge_name, None),
            data.get(response_name, None)
        ]

    def is_nocaptcha(self, data=None):
        if not hasattr(self, "_is_nocaptcha"):
            if data:
                self._is_nocaptcha = self.nocaptcha_response_name in data
            else:
                self._is_nocaptcha = getattr(settings, "NOCAPTCHA", False)
        return self._is_nocaptcha