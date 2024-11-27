from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

@login_required(login_url='/auth/login/')
def user_profile(request):
    user_profile_form=UserProfileForm(instance=request.user)
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST,instance=request.user)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return redirect('/user/my-profile/')
        else:
            for field,error in user_profile_form.errors.items():
                messages.error(request,error)
                break
            
    user = request.user  
    
    return render(request, "userprofile.html", {"user": user, "profile_form": user_profile_form})
    
    
    



