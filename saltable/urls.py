"""saltable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tableid import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/(?P<info>[\w|\W]+)$', views.index, name='index'),
    url(r'^tableentityid/', views.tableEntityId, name='tableEntityId'),
    url(r'^activeTables/', views.activeTables, name='activeTables'),
    url(r'^sitesurvey/$', views.sitesurvey, name='sitesurvey'),
    url(r'^sitesurvey/sitesurvey.sls', views.downloadSiteSurvey, name='downloadSiteSurvey'),
    url(r'^uploadpp/', views.uploadPP, name='uploadpp'),
    url(r'^installpp/$', views.installPP, name='installpp'),
    url(r'^beginInstallPP/', views.beginInstallPP, name='beginInstallPP'),
    url(r'^installpp/activeInstallPP/(?P<position>[\d]+)$', views.activeInstallPP, name='activeInstallPP'),
    url(r'^checkJobStatus/', views.checkJobStatus, name='checkInstallStatus'),
    url(r'^checkInstallFile/$', views.installFileFound, name='checkInstallFile'),
    url(r'^installpp/listlogfiles/', views.listlogfiles, name='listlogfiles'),
    url(r'^installpp/showlogfile/(?P<filename>[\w|\W]+)$', views.showlogfile, name='showlogfile'),
    url(r'^downloadlogfile/(?P<filename>[\w|\W]+)$', views.downloadlogfile, name='downloadlogfile'),
    url(r'^validation/$', views.validation, name='validation'),
    url(r'^validation/beginValidationPP/', views.beginValidationPP, name='beginValidationPP'),
    url(r'^validation/activeValidationPP/(?P<position>[\d]+)$', views.activeValidationPP, name='activeValidationPP'),
    url(r'^filemanage/$', views.filemanage, name='filemanage'),
    url(r'^installwizard/$', views.installwizard, name='installwizard'),
    url(r'^installwizard/startinstall/$', views.startinstall, name='startinstall'),
    url(r'^review/$', views.review, name='review'),
    url(r'^finishinstall/$', views.finishinstall, name='finishinstall'),
    url(r'^admin/', admin.site.urls),
]
