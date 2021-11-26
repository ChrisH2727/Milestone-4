from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages

@login_required
def profile(request):
    """
    Display the user's profile.
    """

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():   
            form.save()
            messages.success(request, 'Your profile has been updated.')
            if not profile.is_registered:
                profile.credits = 10
                profile.is_registered = True
                profile.trees = 0
                profile.tree_count = 0
                profile.save()
                messages.success(request, 'Welcome to Agiview, \
                    we have awarded you 10 free credits')

        else:
            messages.error(request, 'Your profile has not been updated.')
    else:
        form = UserProfileForm(instance=profile)
    
    user_credits = profile.credits
    trees_planted = profile.trees

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'user_credits': user_credits,
        'trees_planted': trees_planted,
    }

    return render(request, template, context)
