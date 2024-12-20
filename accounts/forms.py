from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
        
        # تعريب الحقول
        self.fields['old_password'].label = 'كلمة المرور الحالية'
        self.fields['new_password1'].label = 'كلمة المرور الجديدة'
        self.fields['new_password2'].label = 'تأكيد كلمة المرور الجديدة'

class AdminPasswordChangeForm(SetPasswordForm):
    """
    نموذج لتغيير كلمة المرور من لوحة الإدارة
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'vTextField'})
        self.fields['new_password2'].widget.attrs.update({'class': 'vTextField'})
        
        # تعريب الحقول
        self.fields['new_password1'].label = 'كلمة المرور الجديدة'
        self.fields['new_password2'].label = 'تأكيد كلمة المرور الجديدة'
