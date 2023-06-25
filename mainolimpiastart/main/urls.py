from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', LoginUser.as_view(), name='login'),
    path('logout/', LoginUser.as_view(), name='logout'),
    path('index/', EventListView.as_view(), name='index'),
    path('indiv/', indiv, name='indiv'),
    path('indiv_detail/<str:slug>/', IndivDetailView.as_view(), name='indiv_detail'),
    path('indiv_create/', IndivUpdateView.as_view(), name='indiv_create'),
    path('payment/', payment, name='payment'),
    path('documents/', DocumentsUpdateView.as_view(), name='documents'),
    path('attendance/', attendance, name='attendance'),
    path('notifications/', notifications, name='notifications'),
    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('schedule/<slug:schedule_id>', schedule, name='schedule'),
    path('newsimage/<slug:news_id>/', newsimage, name='newsimage'),
    # path("django-filter.html", views.EventListView.as_view(), name="django-filter"),
]
