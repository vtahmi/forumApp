from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from posts import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('welcome/', views.welcome_message, name='welcome'),
    path('navigation/', views.navigation_view, name='navigation'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('redirect/', views.MyRedirectView.as_view(), name='redirect'),

    path(
        'post/', include([
            path('add/', views.AddPostView.as_view(), name='add-post'),
            path('edit/<int:pk>/', views.EditPostView.as_view(), name='edit-post'),
            path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete-post'),
            path('details/<int:pk>/', views.PostDetailsView.as_view(), name='post-details'),
        ])),
]


