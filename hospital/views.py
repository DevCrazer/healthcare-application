import email
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, PatientForm
from hospital.models import Hospital_Information, User, Patient

from hospital_admin.models import hospital_department, specialization, service
from django.views.decorators.cache import cache_control
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

from .models import Patient, User
from doctor.models import Doctor_Information, Appointment

from sslcommerz.models import Payment
from django.db.models import Q, Count
import re

# Create your views here.

# function to return views for the urls

@login_required(login_url="login")
def hospital_home(request):
    doctors = Doctor_Information.objects.all() 
    context = {'doctors': doctors} 
    return render(request, 'index-2.html', context)

@login_required(login_url="login")
def change_password(request):
    return render(request, 'change-password.html')

@login_required(login_url="login")
def add_billing(request):
    return render(request, 'add-billing.html')

@login_required(login_url="login")
def appointments(request):
    return render(request, 'appointments.html')

@login_required(login_url="login")
def edit_billing(request):
    return render(request, 'edit-billing.html')

@login_required(login_url="login")
def edit_prescription(request):
    return render(request, 'edit-prescription.html')

@login_required(login_url="login")
def forgot_password_patient(request):
    return render(request, 'forgot-password-patient.html')

@login_required(login_url="login")
def privacy_policy(request):
    return render(request, 'privacy-policy.html')

@login_required(login_url="login")
def about_us(request):
    return render(request, 'about-us.html')

@login_required(login_url="login")
def forgot_password_doctor(request):
    return render(request, 'forgot-password-doctor.html')


# def multiple_hospital(request):
#     return render(request, 'multiple-hospital.html')
@login_required(login_url="login")
def chat(request, pk):
    patient = Patient.objects.get(user_id=pk)
    doctors = Doctor_Information.objects.all()

    context = {'patient': patient, 'doctors': doctors}
    return render(request, 'chat.html', context)

@login_required(login_url="login")
def chat_doctor(request):
    if request.user.is_doctor:
        doctor = Doctor_Information.objects.get(user=request.user)
        patients = Patient.objects.all()
        
    context = {'patients': patients, 'doctor': doctor}
    return render(request, 'chat-doctor.html', context)

@login_required(login_url="login")
def hospital_profile(request, pk):
    if request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        doctors = Doctor_Information.objects.all()
        hospitals = Hospital_Information.objects.get(hospital_id=pk)
        
        departments = hospital_department.objects.filter(hospital=hospitals)
        specializations = specialization.objects.filter(hospital=hospitals)
        services = service.objects.filter(hospital=hospitals)
        
        # departments = re.sub("'", "", departments)
        # departments = departments.replace("[", "")
        # departments = departments.replace("]", "")
        # departments = departments.replace(",", "")
        # departments_array = departments.split()
        
        # specializations = re.sub("'", "", specializations)
        # specializations = specializations.replace("[", "")
        # specializations = specializations.replace("]", "")
        # specializations = specializations.replace(",", "")
        # specializations_array = specializations.split()
        
        # services = re.sub("'", "", services)
        # services = services.replace("[", "")
        # services = services.replace("]", "")
        # services = services.replace(",", "")
        # services_array = services.split()
        
        
        
        
        
        context = {'patient': patient, 'doctors': doctors, 'hospitals': hospitals, 'departments': departments, 'specializations': specializations, 'services': services}
        return render(request, 'hospital-profile.html', context)
    else:
        redirect('logout')
@login_required(login_url="login")
def pharmacy_shop(request):
    return render(request, 'pharmacy/shop.html')


# def login(request):
#     return render(request, 'login.html')

# def authenticate_user(email, password):
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return None
#     else:
#         if user.check_password(password):
#             return user


def login_user(request):
    page = 'patient_login'
    if request.method == 'GET':
        return render(request, 'patient-login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_patient:          
                return redirect('patient-dashboard')
            else:
                messages.error(request, 'Invalid credentials. Not a Patient')
                return redirect('logout')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'patient-login.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User Logged out')
    return redirect('login')

@login_required(login_url="login")
def patient_register(request):
    page = 'patient-register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            # commit=False --> don't save to database yet (we have a chance to modify object)
            user = form.save(commit=False)
            user.is_patient = True
            # user.username = user.username.lower()  # lowercase username
            user.save()

            messages.success(request, 'User account was created!')

            # After user is created, we can log them in
            #login(request, user)
            return redirect('login')

        else:
            messages.error(
                request, 'An error has occurred during registration')
    # else:
    #     form = CustomUserCreationForm()

    context = {'page': page, 'form': form}
    return render(request, 'patient-register.html', context)

@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def patient_dashboard(request):
    if request.user.is_patient:
        patient = Patient.objects.get(user=request.user)
        # patient = Patient.objects.get(user_id=pk)
        # appointments = Appointment.objects.filter(patient=patient)
        appointments = Appointment.objects.filter(patient=patient).filter(Q(appointment_status='pending') | Q(appointment_status='confirmed'))
        payments = Payment.objects.filter(patient=patient).filter(appointment__in=appointments).filter(payment_type='appointment')

        context = {'patient': patient, 'appointments': appointments, 'payments': payments}
    else:
        return redirect('logout')
        
    return render(request, 'patient-dashboard.html', context)


# def profile_settings(request):
#     if request.user.is_patient:
#         # patient = Patient.objects.get(user_id=pk)
#         patient = Patient.objects.get(user=request.user)
#         form = PatientForm(instance=patient)  

#         if request.method == 'POST':
#             form = PatientForm(request.POST, request.FILES,instance=patient)  
#             if form.is_valid():
#                 form.save()
#                 return redirect('patient-dashboard')
#             else:
#                 form = PatientForm()
#     else:
#         redirect('logout')

#     context = {'patient': patient, 'form': form}
#     return render(request, 'profile-settings.html', context)
@login_required(login_url="login")
def profile_settings(request):
    if request.user.is_patient:
        # patient = Patient.objects.get(user_id=pk)
        patient = Patient.objects.get(user=request.user)
        old_featured_image = patient.featured_image
        
        if request.method == 'GET':
            context = {'patient': patient}
            return render(request, 'profile-settings.html', context)
        elif request.method == 'POST':
            if 'featured_image' in request.FILES:
                featured_image = request.FILES['featured_image']
            else:
                featured_image = old_featured_image
                
            name = request.POST.get('name')
            dob = request.POST.get('dob')
            age = request.POST.get('age')
            blood_group = request.POST.get('blood_group')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            nid = request.POST.get('nid')
            history = request.POST.get('history')
            
            patient.name = name
            patient.age = age
            patient.phone_number = phone_number
            patient.address = address
            patient.blood_group = blood_group
            patient.history = history
            patient.dob = dob
            patient.nid = nid
            patient.featured_image = featured_image
            
            patient.save()
            return redirect('patient-dashboard')
    else:
        redirect('logout')  

@login_required(login_url="login")
def search(request):
    if request.user.is_patient:
        # patient = Patient.objects.get(user_id=pk)
        patient = Patient.objects.get(user=request.user)
        doctors = Doctor_Information.objects.all()
    else:
        redirect('logout')
        
    context = {'patient': patient, 'doctors': doctors}
    return render(request, 'search.html', context)

def checkout_payment(request):
    return render(request, 'checkout.html')
@login_required(login_url="login")
def multiple_hospital(request):
    if request.user.is_patient:
        # patient = Patient.objects.get(user_id=pk)
        patient = Patient.objects.get(user=request.user)
        doctors = Doctor_Information.objects.all()
        hospitals = Hospital_Information.objects.all()
        
    
        context = {'patient': patient, 'doctors': doctors, 'hospitals': hospitals}
        return render(request, 'multiple-hospital.html', context)
    else:
        redirect('logout')
    
def data_table(request):
    return render(request, 'data-table.html')
