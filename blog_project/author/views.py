from django.shortcuts import render, redirect
from author . forms import RegistrationForm, ChangeUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from posts . models import Post
# Create your views here.


def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Account Created Successfully!')
                return redirect('register')
        else:
            register_form = RegistrationForm()
        return render(request, './author/register.html', {'form' : register_form, 'type' : 'Register'})
    else:
        return redirect("profile")


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            login_form = AuthenticationForm(request, request.POST)
            if login_form.is_valid():
                user_name = login_form.cleaned_data['username']
                user_pass = login_form.cleaned_data['password']
                user = authenticate(username=user_name, password=user_pass)
                if user is not None:
                    messages.success(request, 'Logged in Successfully!')
                    login(request, user)
                    return redirect('profile')
                else:
                    messages.warning(request, 'Login Information Incorrect!')
                    return redirect('register')
        else:
            login_form = AuthenticationForm()
        return render(request, './author/register.html', {'form' : login_form, 'type' : 'Login'})
    else:
        return redirect('profile')


@login_required
def profile(request):
    data = Post.objects.filter(author=request.user)
    return render(request, './author/profile.html', {'data' : data})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ChangeUserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('edit_profile')
    else:
        profile_form = ChangeUserForm(instance=request.user)
    return render(request, './author/update_profile.html', {'form' : profile_form, 'type' : 'Update Profile'})

@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully!')
            update_session_auth_hash(request, form.user)
            return redirect('password_change')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, './author/password_change.html', {'form' : form, 'type' : 'Change Password'})


def user_logout(request):
    logout(request)
    return redirect('user_login')