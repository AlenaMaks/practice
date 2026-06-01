from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.db.models import Count, F
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import (Practice, Application, ApplicationStatus)

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("student_profile")
    else:
        form = ProfileForm(instance=user)

    approved_application = Application.objects.filter(
        student=user,
        status=ApplicationStatus.APPROVED
    ).select_related(
        "practice",
        "practice__company"
    ).first()

    practice = None

    if approved_application:
        practice = approved_application.practice

        practice.skills_list = [
            s.strip()
            for s in practice.skills.split(",")
            if s.strip()
        ]

    return render(
        request,
        "student/profile.html",
        {
            "form": form,
            "practice": practice,
        }
    )

@login_required
def search_view(request):

    if not request.user.profile_completed:
        return redirect("student_profile")

    practices = Practice.objects.filter(
        is_active=True,
        is_archived=False
    ).annotate(
        applications_count=Count("applications")
    )

    company = request.GET.get("company")
    skill = request.GET.get("skill")
    free = request.GET.get("free")

    if company:
        practices = practices.filter(
            company__name__icontains=company
        )

    if skill:
        practices = practices.filter(
            skills__icontains=skill
        )

    if free:
        practices = practices.filter(
            applications_count__lt=F("places")
        )

    for practice in practices:
        practice.skills_list = [
            s.strip()
            for s in practice.skills.split(",")
            if s.strip()
        ]

    user_application = Application.objects.filter(
        student=request.user,
        status__in=[
            ApplicationStatus.PENDING,
            ApplicationStatus.APPROVED
        ]
    ).first()

    return render(
        request,
        "student/search.html",
        {
            "practices": practices,
            "user_application": user_application,
        }
    )

@login_required
def practice_view(request):
    return render(request, 'student/practice.html')

@login_required
def documents_view(request):
    if not request.user.has_active_practice:
        return redirect('student_profile')
    return render(
        request,
        'student/documents.html'
    )

@login_required
def chat_view(request):
    return render(request, 'student/chat.html')

@login_required
def notifications_view(request):
    return render(request, 'student/notifications.html')

@login_required
def apply_practice(request, practice_id):

    if request.method != "POST":
        return redirect("student_search")

    practice = get_object_or_404(
        Practice,
        id=practice_id
    )

    active_application = Application.objects.filter(
        student=request.user,
        status__in=[
            ApplicationStatus.PENDING,
            ApplicationStatus.APPROVED
        ]
    ).exists()

    if active_application:

        messages.error(
            request,
            "У вас уже есть активная заявка."
        )

        return redirect("student_search")

    Application.objects.create(
        student=request.user,
        practice=practice
    )

    messages.success(
        request,
        "Заявка успешно отправлена."
    )

    return redirect("student_search")

@login_required
def cancel_application(request, application_id):

    application = Application.objects.get(
        id=application_id,
        student=request.user
    )

    if application.status == ApplicationStatus.PENDING:
        application.delete()

    return redirect("student_search")
