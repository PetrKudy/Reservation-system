from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views.generic import FormView, ListView, DetailView, CreateView
from django.core.mail import send_mail , EmailMessage
from club.models import PostList,ReservationDate
from club.forms import ContactForm, PostForm , PersonInfoForm, ReservationCancel, JoinUsForm
from django.forms import ModelForm
from django.urls import reverse_lazy
from club.models import ReservationDate, PersonInfo
from django.db import connection
from django.shortcuts import get_object_or_404
import string
import random






class IndexView(TemplateView):
    template_name = 'index.html'

class PhotogalleryView(TemplateView):
    template_name = 'photogallery.html'

class ThanksView(TemplateView):
    template_name = 'thanks.html'

class ContactView(TemplateView):
    template_name = 'contacts.html'

    def get(self,request):
        form = ContactForm
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = ContactForm(request.POST)
        if form.is_valid():
            sur_name = form.cleaned_data['sur_name']
            last_name = form.cleaned_data['last_name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            my_email = 'djangosportcenter@gmail.com'
            user_email = form.cleaned_data['your_email']
            message_to_me =  'email from: '+ sur_name + ' ' + last_name +'\nemail: ' + user_email +'\n\n' +message +'\n\nThis email was generated by form on webpage'
# this send email to sportcenter with question
            send_mail(subject,
                      message_to_me,
                      my_email,
                      [my_email],
                      fail_silently = False)
# this send email to user with thanks message
            send_mail('sportcenter reply',
                      'Thanks for contact, \n\n  We will answer ur question as fast as possible \n\n     Sport center team \n\n\n\nThis email was send by autosend system \n please do not respond to this email',
                      my_email,
                      [user_email],
                      fail_silently = False)
        return render(request,'thanks.html')


class FeedBackView(ListView,FormView):
    # Display
    template_name = 'feedback.html'
    model = PostList
    context_object_name = 'PostList'
    queryset = PostList.objects.order_by('-post_created')
    paginate_by = 20
    # form
    form_class = PostForm
    success_url = reverse_lazy('feedback')

    def form_valid(self,form):
        form.save()
        return super().form_valid(form)

class ReservationView(ListView):
    template_name = 'reservation.html'
    model = ReservationDate
    context_object_name = 'reservation_date'






class ReservationTimeView(DetailView,FormView):
    template_name = 'reservationtimes.html'
    model = ReservationDate
    queryset = ReservationDate.objects.all()
    form_class = PersonInfoForm
    success_url = '../../reservation_complete'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(ReservationTimeView, self).get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs

    def form_valid(self,form):
        person_info = form.cleaned_data

        reservation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) # generate random code
        try:
            reservation_id = PersonInfo.objects.latest('reservation_id').reservation_id + 1 # get first empty pk
        except: # if database is empty, then set 1
            reservation_id = 1
        #save person
        person_model_make = PersonInfo( reservation_id = reservation_id,
                                        first_name = person_info['first_name'],
                                        sur_name = person_info['sur_name'],
                                        email = person_info['email'],
                                        mobil_phone = person_info['mobil_phone'],
                                        reservation_code =  reservation_code,
                                        date_id = self.kwargs['pk'])

        person_model_make.save()
        #reserve term in database
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE club_ReservationDate SET {person_info['Time_Select']} = {reservation_id} WHERE day_id = {self.kwargs['pk']}")

        # send email with code
        send_mail('reservation to sportcenter',
                  f'Thanks for reservation\n\n Your code for reservation is {reservation_code} \n\n See You soon!',
                  'djangosportcenter@gmail.com',
                  [person_info['email']],
                  fail_silently = False)
        return render(self.request,'reservation_complete.html',{'code':reservation_code})


class ReservationCompleteView(TemplateView):
    template_name = 'reservation_complete.html'

class PriceView(TemplateView):
    template_name = 'prices.html'


class ReservationCancelView(TemplateView,FormView):
    template_name = 'reservation_cancel.html'
    form_class = ReservationCancel
    success_url = "../../"


    def form_valid(self, form):
        info = form.cleaned_data
        try:
            ids_info = PersonInfo.objects.filter(reservation_code = info['your_code'],email = info['your_email']).values('date_id','reservation_id')[0]# get date info
        except:
            print(form)
            return render(self.request,self.template_name,{'form':form,
                                                            'message':'Your code or email is wrong, please try again or call our support'})

        date_times = ReservationDate.objects.filter(day_id=ids_info['date_id']).values()[0]
        # looking for reserved time
        for key in date_times.keys():
            if date_times[key] == str(ids_info['reservation_id']):
                time_to_change = key

        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE club_ReservationDate SET {time_to_change} = 'open' WHERE day_id = {ids_info['date_id']}") # set default value

            cursor.execute(f"DELETE FROM club_PersonInfo WHERE reservation_id = '{ids_info['reservation_id']}'") # delete person
        return super().form_valid(form)


class JoinUsView(TemplateView,FormView):
    template_name = "joinus.html"
    success_url = "../../"
    form_class =  JoinUsForm


    def form_valid(self,form):
        info = form.cleaned_data
        print(info)
        mail = EmailMessage(info['subject'],
                            f"From: {info['sur_name']} {info['last_name']}\nemail:{info['your_email']}\n\n{info['message']}",
                            'djangosportcenter@gmail.com',
                            ['djangosportcenter@gmail.com'],)
        mail.attach(info['file'].name, info['file'].read(), info['file'].content_type)
        mail.send()
        return super().form_valid(form)
