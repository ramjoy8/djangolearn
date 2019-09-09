from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import logging
from eventapp.admin import UserCreationForm
from eventapp.models import AddEventForm,MyUser,Events
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.

def home(request,email=None) :
    logger.info(request.method)
    
    eventsall=Events.objects.all()
    
    if request.method=="POST" :
        email=request.POST['email']
        passw=request.POST['passw']
        user=authenticate(request,username=email,password=passw)
        if user is not None :
            login(request,user)
            eventsall=Events.objects.filter(created_by=user)
            return render(request,'userlogin.html',{
                'user':user,

                'eventsall':eventsall
            })
        else :
            errormsg='Wrong Credentials'
            return render(request,'home.html',{
                'errormsg':errormsg,
                'email':email
            })

    return render(request,'home.html',{
        'eventsall' :eventsall,
        'email':email
    })

@login_required(login_url='login')
def addevent(request):
    form=AddEventForm()
    return render(request,'useraddevent.html',{'form':form})

def signup(request) :    
    form=UserCreationForm()
    if request.method=="POST" :
        form=UserCreationForm(request.POST)
        if form.is_valid() and form.clean_password2():
            user=form.save()
            login(request,user)
            eventsall=Events.objects.filter(created_by=user)
            return render(request,'userlogin.html',{ 'user':user,'eventsall':eventsall})

    return render(request,'signup.html',{
    'form':form
})        

def userlogin(request) :

    if request.method=="POST" :
         email=request.POST['email']
         passw=request.POST['passw']
         user=authenticate(request,username=email,password=passw)
         if user is not None :
            login(request,user)
            eventsall=Events.objects.filter(created_by=user)
            return render(request,'userlogin.html',{
                'user':user,
                'eventsall':eventsall
            })
         else :
            errormsg='Wrong Credentials'
            return render(request,'login.html',{
                'errormsg':errormsg,
            })
    return render(request,'login.html')

@login_required(login_url='login')    
def useraddevent(request,email) :

    form=AddEventForm()
    if request.method=="POST" :
        #if form.is_valid() :

                   event=AddEventForm(request.POST).save(commit=False)
                   user=MyUser.objects.get(email=email)
                   event.created_by=user
                   event.save()
                   eventsall=Events.objects.filter(created_by=user)
                   return  render(request,'userlogin.html',{
                         'eventsall':eventsall})    
    return render(request,'useraddevent.html',{'form':form})                           

def userlogout(request) :

    logout(request)
    return redirect('/')
