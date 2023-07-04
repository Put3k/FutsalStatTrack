from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

from .forms import RegisterUserForm

def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.success(request, ("There Was An Error Logging In, Try Again."))
            return redirect('login')
        
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out Successfully."))
    return redirect('home')


def register_user(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (f"You have successfully registered and logged in."))
            return redirect('home')

    else:
        form = RegisterUserForm()

    context = {
        'form': form,
    }

    return render(request, 'authenticate/register_user.html', context=context)



