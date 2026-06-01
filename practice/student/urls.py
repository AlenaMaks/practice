from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='student_profile'),
    path('search/', views.search_view, name='student_search'),
    path('practice/', views.practice_view, name='student_practice'),
    path('documents/', views.documents_view, name='student_documents'),
    path('chat/', views.chat_view, name='student_chat'),
    path('notifications/', views.notifications_view, name='student_notifications'),
    path("practice/<int:practice_id>/apply/", views.apply_practice, name="apply_practice"),
    path("application/<int:application_id>/cancel/", views.cancel_application, name="cancel_application"),
]