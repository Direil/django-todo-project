from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import ProfileForm


def register_user(request):

    if request.user.is_authenticated:
        return redirect("list")

    form = ProfileForm()

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list')
        else:
            messages.warning(request, 'An error occurred during registration')

    return render(request, 'profile/register.html', {'form': form})
