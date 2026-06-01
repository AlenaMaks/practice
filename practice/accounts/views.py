from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ProfileForm
from django.contrib import messages

from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("student_profile")

    form = LoginForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                login(request, user)
                return redirect("student_profile")

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные сохранены")
            return redirect("student_profile")
    else:
        form = ProfileForm(instance=user)

    return render(
        request,
        "student/profile.html",
        {
            "form": form,
            "user": user
        }
    )