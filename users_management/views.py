from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('/login')
        else:
            messages.error(request, 'Something went wrong')
    else:
        form = NewUserForm()
    
    return render(request, "register.html", {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('/feed')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/feed')
        else:
            messages.error(request, "Invalid username/password")

    form = AuthenticationForm()
    return render(request, "login.html", {'form': form })

def signout(request):
    logout(request)
    return redirect('/login')
