from django import forms
from django.contrib.auth.models import User
from account.models import Doctors,Patients
from account.validators import valid_no
class DoctorUserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(),help_text="Set your own password")
    username=forms.CharField(max_length=50,help_text='Set your own username. Required. Letters, digits and @/./+/-/_ only.')
    class Meta():
        model=User
        fields=('username','email','password')
class DoctorProfileForm(forms.ModelForm):
    contact_no=forms.CharField(max_length=10,min_length=10,help_text="10 digit mobile number",validators=[valid_no])
    class Meta():
        model=Doctors
        fields=("name","clinic_name","qualf","special","contact_no")
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['qualf'].label="Qualification"
        self.fields['special'].label="Specialisation"

class PatientUserForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': ("User with this mobile number already exists! If registered already please login otherwise register with different number"),
        'max_length': 'Enter 10 digits only',
        'min_length': 'Enter 10 digits'

    }
    username=forms.CharField(max_length=10,min_length=10,help_text="10 digit mobile number",
                             validators=[valid_no],error_messages=error_messages)
    class Meta():
        model=User
        fields=('username',)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        if self.instance.username == username:
            return username
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Mobile number"


class PatientProfileForm(forms.ModelForm):
    class Meta():
        model=Patients
        fields=("name","age")


