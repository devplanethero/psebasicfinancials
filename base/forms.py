from django import forms
from .models import Feedback
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), required=True)