from django.urls import path
from . import views

urlpatterns = [

path('',views.home,name='home' ),
path('/<str:email>',views.home,name="userhome"),

path('signup',views.signup,name='signup'),
path('login',views.userlogin,name='login'),
path('logout',views.userlogout,name='logout'),
path('user/useraddevent/<str:email>/',views.useraddevent,name='useraddevent'),
]