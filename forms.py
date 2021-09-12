from django import forms
from .models import *


class Organisation_Form(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = '__all__'


class Internship_Form(forms.ModelForm):
    berid              = forms.ChoiceField(choices=berids, required=False)
    class Meta:
        model = Internship
        exclude = ('organisation',)
        fields = '__all__'

        
class InternshipAssignments_Form(forms.ModelForm):
    class Meta:
        model = InternshipAssignment
        exclude = ('schoolyear','internship')
        fields = '__all__'