"""loyalty_program URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from loyalty_program.apps.referral.views import GetUserReferralsView, UpdateUserView, GetReferralsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/<str:cpf>/', UpdateUserView.as_view()),
    path('all-referrals/', GetReferralsView.as_view()),
    path('all-referrals/<str:cpf>/', GetUserReferralsView.as_view()),
]
