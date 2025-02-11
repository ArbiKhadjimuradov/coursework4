from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView, UserConfirmEmailView, EmailConfirmationSentView, EmailConfirmedView, \
    EmailConfirmationFailedView, UserForgotPasswordView, UserPasswordResetConfirmView, LoginUserView, LogoutUserView, \
    ProfileUserDetailView, ProfileUserUpdateView


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutUserView.as_view(next_page='SendMailService:home'), name='logout'),

    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('profile/<int:pk>/', ProfileUserDetailView.as_view(), name='profile_user'),
    path('<int:pk>/profile_edit/', ProfileUserUpdateView.as_view(), name='profile_edit'),
]