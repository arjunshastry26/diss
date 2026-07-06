from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import StyledAuthenticationForm

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='forum/login.html', authentication_form=StyledAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('discussion/new/', views.create_discussion_view, name='create_discussion'),
    path('discussion/<int:pk>/', views.discussion_detail_view, name='discussion_detail'),
    path('discussion/<int:pk>/edit/', views.edit_discussion_view, name='edit_discussion'),
    path('discussion/<int:pk>/delete/', views.delete_discussion_view, name='delete_discussion'),
    path('discussion/<int:pk>/resolve/', views.toggle_resolved_view, name='toggle_resolved'),
    path('discussion/<int:pk>/like/', views.toggle_like_view, name='toggle_like'),

    path('comment/<int:pk>/solution/', views.mark_solution_view, name='mark_solution'),
    path('comment/<int:pk>/delete/', views.delete_comment_view, name='delete_comment'),

    path('category/<int:pk>/', views.category_view, name='category_detail'),

    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]
