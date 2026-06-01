from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'student/profile.html')

@login_required
def search_view(request):

    if not request.user.profile_completed:
        return redirect('student_profile')

    return render(
        request,
        'student/search.html'
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
