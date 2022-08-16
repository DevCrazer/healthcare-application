from unicodedata import name
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# from . --> same directory
# Views functions and urls must be linked. # of views == # of urls
# App URL file - urls related to hospital


urlpatterns = [
    path('', views.hospital_home, name='hospital_home'),
    path('search/', views.search, name='search'),
    path('change-password/', views.change_password, name='change-password'),

    path('add-billing/', views.add_billing, name='add-billing'),

    path('appointments/', views.appointments, name='appointments'),

    path('edit-billing/', views.edit_billing, name='edit-billing'),
    path('edit-prescription/', views.edit_prescription, name='edit-prescription'),
    path('forgot-password-patient/', views.forgot_password_patient,name='forgot-password-patient'),
    path('patient-dashboard/',views.patient_dashboard, name='patient-dashboard'),
    
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    # path('profile-settings/', views.profile_settings, name='profile-settings'),
    path('profile-settings/',views.profile_settings, name='profile-settings'),

    path('about-us/', views.about_us, name='about-us'),
    path('patient-register/', views.patient_register, name='patient-register'),
    path('logout/', views.logoutUser, name='logout'),
    path('forgot-password-doctor/', views.forgot_password_doctor,name='forgot-password-doctor'),

    path('multiple-hospital/', views.multiple_hospital, name='multiple-hospital'),
    path('chat/<int:pk>/', views.chat, name='chat'),
    path('chat-doctor/', views.chat_doctor, name='chat-doctor'),

    path('hospital-profile/', views.hospital_profile, name='hospital-profile'),
    path('checkout-payment/', views.checkout_payment, name='checkout-payment'),
    path('shop/', views.pharmacy_shop, name='pharmacy_shop'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
