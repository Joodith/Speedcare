from django.conf.urls import url
from django.contrib.auth import views as auth_views
from account import views
app_name="account"
urlpatterns=[
    url(r'^doctor_register/$',views.doctor_register,name="doc_reg"),
    url(r'^doctor_login/$',views.doctor_user_login,name="doc_user_login"),
    url(r'^patient_register/$',views.patient_register,name="pat_reg"),
    url(r'^patient_login/$',views.patient_user_login,name="pat_user_login"),
    url(r'^logout/$',auth_views.LogoutView.as_view(),name="logout"),
    url(r'^home/$', views.DoctorHomeView.as_view(), name="doctor_home"),
    url(r'^doctor_list/$',views.DoctorListView.as_view(),name="list_doctor"),
    url(r'^doctor_detail/(?P<username>[-\w]+)/(?P<pk>\d+)/$',views.DoctorDetailView.as_view(),name="detail_doctor"),
    url(r'^clinic_list/$',views.ClinicListView.as_view(),name="list_clinic"),


]