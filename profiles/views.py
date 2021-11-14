from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm, RegistrationProfileForm
from pprint import pprint
from django.contrib import messages


def profile(request):
    """
    Display the user's profile. 
    """

    profile= get_object_or_404(UserProfile, user=request.user)
    #default_profile= get_object_or_404(User, username=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        #default_form = UserProfileForm(request.POST, instance=default_profile)
        #if form.is_valid() & default_form.is_valid():
        if form.is_valid():   
            form.save()
            #default_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
        #default_form = RegistrationProfileForm(instance=default_profile)
    
    pprint(vars(profile))
    # pprint(vars(default_profile))

    form= UserProfileForm(instance=profile)
    #default_form = RegistrationProfileForm(instance=default_profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        #'default_form': default_form,
    }

    return render(request, template, context)
