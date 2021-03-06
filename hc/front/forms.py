from django import forms
from hc.api.models import Channel
from .validators import CronScheduleValidator


class NameTagsForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=500, required=False)

    def clean_tags(self):
        l = []

        for part in self.cleaned_data["tags"].split(" "):
            part = part.strip()
            if part != "":
                l.append(part)

        return " ".join(l)


class TimeoutForm(forms.Form):
    timeout = forms.IntegerField(min_value=60, max_value=7776000)
    grace = forms.IntegerField(min_value=60, max_value=7776000)


class AdvancedCronForm(forms.Form):
    grace = forms.IntegerField(min_value=1, max_value=7776000)
    cron_schedule = forms.CharField(max_length=100, validators=[CronScheduleValidator()])


class AddChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = ['kind', 'value', 'username', 'apikey']

    def clean_value(self):
        value = self.cleaned_data["value"]
        return value.strip()


class AddWebhookForm(forms.Form):
    error_css_class = "has-error"

    value_down = forms.URLField(max_length=1000, required=False)
    value_up = forms.URLField(max_length=1000, required=False)

    def get_value(self):
        return "{value_down}\n{value_up}".format(**self.cleaned_data)
