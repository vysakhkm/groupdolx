from django.urls import path
from olxweb import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns= [
    path("signup",views.Signupview.as_view(),name="register"),
    path("",views.LoginView.as_view(),name="signin"),
    path("home",views.homeview.as_view(),name="home"),
    path("signout",views.Signoutview.as_view(),name="signout"),
    path("profile/add",views.Userprofilecreateview.as_view(),name="profile-add"),
    path("profile",views.Profiledetailview.as_view(),name="profile_detail"),
    path("profile/<int:id>/change",views.Profileupdateview.as_view(),name="profile-change")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)