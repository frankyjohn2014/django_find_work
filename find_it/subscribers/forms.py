from django import forms
from subscribers.models import Subscribers
from subscribers.models import Speciality, City

class SubscriberModelForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    speciality = forms.ModelChoiceField(label='Специальность', queryset=Speciality.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Subscribers
        fields = ('email','city','speciality','password',)
        exclude = ('is_active',)

class LogInForm(forms.Form):
    email = forms.EmailField(label='E-mail',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_password(self,*args,**kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            qs = Subscribers.objects.filter(email=email).first()
            if qs == None:
                raise forms.ValidationError("""Пользователя с таким email не существует""")
            elif password != qs.password:
                raise forms.ValidationError("""Неверный пароль""")
        
        return email


class SubscribersHiddenEmailForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail',required=True, widget=forms.HiddenInput())
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    speciality = forms.ModelChoiceField(label='Специальность', queryset=Speciality.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    is_active = forms.BooleanField(label='Получать рассылку?', required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Subscribers
        fields = ('email','city','speciality','password', 'is_active')