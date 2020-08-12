from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView,CreateView,DetailView,ListView,RedirectView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from account.forms import DoctorUserForm,DoctorProfileForm,PatientUserForm,PatientProfileForm
from account.models import Doctors,Clinics,Patients,FixAppt

# Create your views here.
def doctor_register(request):
    registered=False
    if request.method=="POST":
        user_form=DoctorUserForm(data=request.POST)
        reg_form=DoctorProfileForm(data=request.POST)
        if user_form.is_valid() and reg_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            reg=reg_form.save(commit=False)
            reg.user=user
            reg.save()
            registered=True
            return redirect('account:doc_user_login')
        else:
            messages.error(request, 'Change the username!')
    else:
        user_form=DoctorUserForm()
        reg_form=DoctorProfileForm()
    return render(request,"registration/doctor_registration.html",{'user_form':user_form,'reg_form':reg_form,'registered':registered})

def doctor_user_login(request):
    if request.method=="POST":
        form = AuthenticationForm(request, request.POST)
        username=request.POST.get('username')
        password= request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            login(request,user)

            return redirect('account:doctor_home')
        else:
            messages.error(request, 'Invalid username and password')
    else:
        form = AuthenticationForm(request)
    return render(request,"registration/doctor_login.html",{'form':form})

def patient_register(request):
    registered=False
    if request.method=="POST":
        base_form=PatientUserForm(data=request.POST)
        pat_form=PatientProfileForm(data=request.POST)
        if base_form.is_valid() and pat_form.is_valid():
            user = base_form.save()
            user.set_password(user.password)
            user.save()
            pat=pat_form.save(commit=False)
            pat.user=user
            pat.save()
            registered=True
            return HttpResponseRedirect(reverse('account:pat_user_login'))
        else:
            messages.error(request, '')

    else:
        base_form=PatientUserForm()
        pat_form=PatientProfileForm()
    return render(request,"registration/patient_registration.html",{'base_form':base_form,'pat_form':pat_form,'registered':registered})

def patient_user_login(request):
    if request.method=="POST":
        form=AuthenticationForm(request,request.POST)
        username = request.POST.get('username')
        if not User.objects.filter(username=username):
            messages.error(request, 'User with the mobile number does not exist!')
            return HttpResponseRedirect(reverse('account:pat_user_login'))
        user = User.objects.get(username=username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request,'User with the mobile number does not exist!')
            return HttpResponseRedirect(reverse('account:pat_user_login'))
    else:
        form=AuthenticationForm(request)
        return render(request,"registration/patient_login.html",{'form':form})

## DOCTOR VIEWS

class DoctorListView(ListView):
    context_object_name ="listdoc"
    model=Doctors
    template_name ="doctor/doctor_list.html"

class DoctorDetailView(DetailView):
    context_object_name="detdoc"
    model=Doctors
    template_name="doctor/doctor_detail.html"
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class DoctorHomeView(TemplateView,RedirectView):
    template_name="doctor/doctor_base.html"
    def get_redirect_url(self, pk):
        doctors=Doctors.objects.get(pk=pk)
        username=doctors.user.username
        return reverse('account:detail_doctor',args=(username,pk))

class ClinicListView(ListView):
    context_object_name ="clinlist"
    model=Clinics
    def get_queryset(self):
        user = get_object_or_404(Doctors, kwargs={'pk': self.kwargs.get(id)})
        p=Clinics.objects.filter(resp_clinic=self.user.id)
        return p
    template_name="clinic/clinic_list.html"










