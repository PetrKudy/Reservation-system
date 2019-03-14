from django import forms
from django.forms import ModelForm
from django.db.models.expressions import RawSQL
from club.models import PostList, PersonInfo, ReservationDate

class ReservationCancel(forms.Form):

    your_code = forms.CharField(max_length=10)
    your_email = forms.EmailField(max_length=30)

class ContactForm(forms.Form):

    sur_name = forms.CharField(max_length = 70)
    last_name = forms.CharField(max_length = 70)
    your_email = forms.EmailField(max_length = 70)
    subject = forms.CharField(max_length = 50)
    message = forms.CharField(max_length = 400,widget=forms.Textarea)

class PostForm(ModelForm):
    class Meta:
        model = PostList
        fields = ['name','text']
        labels = {'name':'Name or Nickname:',
                'text': 'Message:'

        }

class PersonInfoForm(forms.ModelForm):
    #dynamic field
    def __init__(self,pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # get day info
        hours = list(ReservationDate.objects.filter(day_id=pk).values())[0]

        # display not reserved hours in dropdown box
        free_hours = []
        for key in hours.keys():
            if key == 'T6_7'and hours[key] == 'open':
                free_hours.append((key,'6:00-7:00'))
            elif key == 'T7_8'and hours[key] == 'open':
                free_hours.append((key,'7:00-8:00'))
            elif key == 'T8_9'and hours[key] == 'open':
                free_hours.append((key,'8:00-9:00'))
            elif key == 'T9_10'and hours[key] == 'open':
                free_hours.append((key,'9:00-10:00'))
            elif key == 'T10_11'and hours[key] == 'open':
                free_hours.append((key,'10:00-11:00'))
            elif key == 'T11_12'and hours[key] == 'open':
                free_hours.append((key,'11:00-12:00'))
            elif key == 'T12_13'and hours[key] == 'open':
                free_hours.append((key,'12:00-13:00'))
            elif key == 'T13_14'and hours[key] == 'open':
                free_hours.append((key,'13:00-14:00'))
            elif key == 'T14_15'and hours[key] == 'open':
                free_hours.append((key,'14:00-15:00'))
            elif key == 'T15_16'and hours[key] == 'open':
                free_hours.append((key,'15:00-16:00'))
            elif key == 'T16_17'and hours[key] == 'open':
                free_hours.append((key,'16:00-17:00'))
            elif key == 'T17_18'and hours[key] == 'open':
                free_hours.append((key,'17:00-18:00'))
            elif key == 'T18_19'and hours[key] == 'open':
                free_hours.append((key,'18:00-19:00'))
            elif key == 'T19_20'and hours[key] == 'open':
                free_hours.append((key,'19:00-20:00'))
            elif key == 'T20_21'and hours[key] == 'open':
                free_hours.append((key,'20:00-21:00'))
            elif key == 'T21_22'and hours[key] == 'open':
                free_hours.append((key,'21:00-22:00'))
            elif key == 'T22_23'and hours[key] == 'open':
                free_hours.append((key,'22:00-23:00'))
            elif key == 'T23_24'and hours[key] == 'open':
                free_hours.append((key,'23:00-24:00'))

        self.fields['Time_Select'] = forms.ChoiceField(choices = free_hours)

    class Meta:
        model = PersonInfo
        fields = ['first_name','sur_name','email','mobil_phone']


class JoinUsForm(forms.Form):
    sur_name = forms.CharField(max_length = 70,)
    last_name = forms.CharField(max_length = 70)
    your_email = forms.EmailField(max_length = 70)
    subject = forms.CharField(max_length = 50)
    message = forms.CharField(max_length = 400,widget=forms.Textarea)
    file = forms.FileField()
