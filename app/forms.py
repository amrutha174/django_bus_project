from django import forms
from app.models import Busbooking,BusDetails,Register
class BusForm(forms.ModelForm):
    class Meta:
        model = Busbooking
        fields = ('NAME','EMAIL','PH_NO','USERNAME','PASSWORD')

class BusDetailsForm(forms.ModelForm):
    class Meta:
        model = BusDetails
        fields = ('FROM','TO')
    
class LoginForm(forms.ModelForm):
    class Meta:
        model = Busbooking
        fields = ('USERNAME','PASSWORD')
    

class Otp_Ver(forms.Form):
    # TODO: Define form fields here
    OTP =forms.IntegerField()

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ('CSID','BID')
        
class Confirm(forms.Form):
    Num_Seats = forms.IntegerField()