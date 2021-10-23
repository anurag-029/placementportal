from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .forms import StudentSignUpForm
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def userlogin(request):
    if request.user.is_authenticated:
        render(request,'placementapp/dashboard.html',{'user':request.user})
    else:
        if request.method=="POST":
            form=AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                username=form.cleaned_data.get('username')
                password=form.cleaned_data.get('password')
                varuser=authenticate(username=username,password=password)
                if varuser is not None:
                    login(request,varuser)
                    #messages.info(request,f"You are not logged in as {username}")
                    return render(request,'placementapp/dashboard.html',{'user':varuser})
                else:
                    messages.error(request,f"InValid")
            else:
                messages.error(request,"Invalid username")
        form=AuthenticationForm()
        return render(request,'placementapp/login.html',{'form':form})
            
def userlogout(request):
    logout(request)
    messages.info(request,"You have Successfully logged out")
    redirect("placementapp/dashboard")

def signup(request):
    if request.user.is_authenticated:
        redirect("placementapp/dashboard")
    else:
        if request.method=='POST':
            form=StudentSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                form=StudentSignUpForm()
                #return render(request,'placementapp/signup.html',{'form':form})
        else:
            form=StudentSignUpForm()
        return render(request,'placementapp/signup.html',{'form':form})

def studentdashboard(request):
    return render(request,'placementapp/dashboard.html')
def companydashboard(request):
    pass
def placementoffdashboard(request):
    pass

def getallPosition(request):
    if request.user.is_authenticated and request.user.user_type==1 and request.user.verified:
        Stu=Student.objects.get(user=request.user)
        if(request.user.verified):
            positions=Position.objects.filter(branch=Stu.Branch)
        else:
            positions=None
    elif request.user.is_authenticated and request.user.user_type==3 and request.user.verified:
        Comp=Company.objects.get(user=request.user)
        positions=Position.objects.filter(Company=Comp)
    elif request.user.is_authenticated and request.user.user_type==2 and request.user.verified:
        positions=Position.objects.all().order_by('branch__Start_year')
    else:
        positions=None
    return positions
        
# def getallOffers(request):
#     if request.user.is_authenticated and request.user.verified:
#         if request.user.user_type==1:
#             Stu=Student.objects.get(user=request.user)
#             offers=Offers.objects.filter(Student=Stu).order_by('FinalCTC')
#         if request.user.user_type==3:
#             comp=Company.objects.get(user=request.user)
#             #positions=Position.objects.filter(Company=comp)
#             offers=Offers.objects.filter(Position__Company=comp)
#         else:
#             offers=None
#     else:
#         offers=None
#     return offers

def getMsg2S(request):
    varuser=request.user
    msg=None
    if varuser.is_authenticated and varuser.user_type==1 and varuser.verified:
        stu=Student.objects.get(user=varuser)
        msg=MessageP2S.objects.filter(receivers=stu).order_by('TimeStamps')
    if varuser.is_authenticated and varuser.user_type==2 and varuser.verified:
        msg=MessageP2S.objects.all().order_by('TimeStamps')
    return msg


def getMsg2C(request):
    varuser=request.user
    msg=None
    if varuser.is_authenticated and varuser.user_type==3 and varuser.verified:
        comp=Company.objects.get(user=varuser)
        msg=MessageP2C.objects.filter(receivers=comp).order_by('TimeStamps')
    if varuser.is_authenticated and varuser.user_type==2 and varuser.verified:
        msg=MessageP2C.objects.all().order_by('TimeStamps')
    return msg
# retrive Msg Recieved By Placement Officer or sended to placementCell by Company
def getMsg2P(request):
#USer VAriable
    varuser=request.user
    msg=None
    #if User is 
    if varuser.is_authenticated and varuser.user_type==3 and varuser.verified:
        comp=Company.objects.get(user=varuser)
        msg=MessageC2P.objects.filter(sender=comp).order_by('TimeStamps')

    if varuser.is_authenticated and varuser.user_type==2 and varuser.verified:
        msg=MessageC2P.objects.all().order_by('TimeStamps')
    return msg

#Create Forms For Below functionalities-
    # send Msg from PlacementOfficer to Company
    # send Msg from PlacementOfficer to Student
    # send Msg from Company to PlacementOfficer  
    # Update Student Details based on Model
    # Update Mentor Detail 
    # Update Company Detail 

# For Company 
# Create New Position -Create A Form and then save it 
# Update Existing Position -Create A form and save the existing Position
# Delete Existing Positions
# Get all student who applied for a particular position and are eligible and not rejected before
def getStudentApplied(request):
    varuser=request.user
    applied=None
    if varuser.is_authenticated and varuser.verified :
        if varuser.user_type==3:
            comp=Company.objects.get(user=varuser)
            applied=Applied.objects.filter(Position__Company=comp)
            return applied
        elif varuser.user_type==1:
            stu=Student.objects.get(user=varuser)
            applied=Applied.objects.filter(Student=stu)
        elif varuser.user_type==2:
            applied=Applied.objects.all().order_by('Time')
        return applied
    return applied
#Update status of Students who are eligible for next round
# Create New Offer for Particular Position -Create A form then save
# Update Existing Offer
#  
# Delete Offer
def deleteOffer(request,id):
    offer=Offers.objects.get(pk=id)
    offer.delete()
    return None
#Update or assign Offer to those Student who applied for the position and got selected



