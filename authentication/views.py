from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm,CustomeLoginForm,ResetPasswordForm,ForgetPasswordForm
from users.models import User
from whatbytes.handle_functions import generate_password
def home_view(request):
    return render(request, "home.html")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully! You can now log in.")
            return redirect("/auth/signup/")  
        else:
            # Collect validation errors and add them to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f" {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, "signupform.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = CustomeLoginForm()  

    if request.method == "POST":
        form = CustomeLoginForm(data=request.POST)  
        if form.is_valid():
            email = form.cleaned_data.get('email')  
            password = form.cleaned_data.get('password')
            print(email, password)
            user = authenticate(request, username=email, password=password)  
            print(user)
            if user is not None:
                
                login(request, user)  
                messages.success(request,"Login Successfully")
                return redirect('/user/my-profile/') 
            else:
                messages.error(request, f" user not found")
        else:
            messages.error(request, "No account found for given credentials")
    return render(request, "loginform.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='./auth/login/')
def reset_password_view(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed successfully. Please log in again.")
            return redirect("/auth/login/")  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ResetPasswordForm(user=request.user)

    return render(request, "resetpassword.html", {"form": form})

def forget_password_view(request):
    if request.method == "POST":
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                
                new_password = generate_password()
                
                user.set_password(new_password)
                user.save()
                messages.success(request, f"A new password has been sent to {email} and your new password is {new_password}.")
                return render(request, "forgetpassword.html", {"new_password": new_password})

            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
        else:
            messages.error(request, "account does not exist")
    
    else:
        form = ForgetPasswordForm()

    return render(request, "forgetpassword.html", {"form": form})
