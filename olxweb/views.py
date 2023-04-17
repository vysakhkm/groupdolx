from django.shortcuts import render,redirect
from django.views.generic import CreateView,TemplateView,FormView,View,UpdateView
from django.contrib.auth.models import User
from olxweb.forms import Registrationform,LoginForm,UserprofileForm
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from api.models import Userprofile
# Create your views here.
def sigin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
decs=[sigin_required,never_cache]

class Signupview(CreateView):
    form_class=Registrationform
    model=User
    template_name="register.html"
    success_url=reverse_lazy("signin")
    def form_valid(self, form):
        messages.success(self.request, "Account created successfully")
        return super().form_valid(form)
class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"account created seccessfully")
                return redirect("home")
            else:
                messages.error(request,"provided credentials are invalid")
                return render(request,"login.html",{"form":form})

@method_decorator(decs,name='dispatch')
class homeview(TemplateView):
    template_name="index.html"

class Userprofilecreateview(CreateView):
    model=Userprofile
    form_class=UserprofileForm
    template_name="profile-add.html"
    success_url=reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
class Profiledetailview(TemplateView):
    template_name="profiledetails.html"

class Profileupdateview(UpdateView):
    model=Userprofile
    template_name="profileupdate.html"
    form_class=UserprofileForm
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"

class Signoutview(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")