from django.urls import path, include
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .views import *
urlpatterns = [
    path('',Index.as_view(), name='index'),
    path('register/', signup_view, name='register' ),
    path('profile/<int:pk>/', login_required(EditProfile.as_view()), name='edit-profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('my-posts/', login_required(MyPosts.as_view()), name='my-posts'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post-detail'),
    path('posted_by/<slug:slug>/', authorSuggestionList.as_view(), name ='author-suggestion-list'),
    path('contributors/', ContributionList.as_view(), name='contribution-list'),
    path('new-post/', login_required(SuggestionCreateView.as_view()), name='create-suggestion'),
    path('f/<slug:filter>/<slug:slug>', SlugSuggestionList.as_view(), name='slug-suggestion-list'),
    path('random/<slug:filter_slug>/<slug:secondary_slug>', random_post, name='random-post'),
    path('edit-post/<slug:slug>/', login_required(SuggestionUpdateView.as_view()), name='edit-post'),
    path('delete-post/<slug:slug>/', login_required(SuggestionDeleteView.as_view()), name='delete-post')
]

""" 
accounts/ django.contrib.auth.urls
path('login/', views.LoginView.as_view(), name='login'),
path('logout/', views.LogoutView.as_view(), name='logout'),

path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), """