from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from bolt.models import Shelter, Animal, UserProfile
from django.contrib.auth.models import User
from bolt.forms import AnimalForm, ShelterForm, UserProfileForm, UserForm, FqaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
import json,os
# Create your views here.
def index(request):
    shelter_list = Shelter.objects.all()
    context_dict = {}
    context_dict['shelters'] = shelter_list

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'pages/home.html', context=context_dict)
    return response

def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'pages/aboutus.html', context=context_dict)

def show_shelter(request, shelter_name_slug):
    context_dict = {}
    try:
        shelter = Shelter.objects.get(slug=shelter_name_slug)
        animals = Animal.objects.filter(shelter=shelter)

        context_dict['shelter'] = shelter
        context_dict['animals'] = animals
    except Shelter.DoesNotExist:
        context_dict['shelter'] = None
        context_dict['animals'] = None
    return render(request, 'pages/shelter.html', context=context_dict)


def add_shelter(request):
    form = ShelterForm()
    if request.method == 'POST':
        form = ShelterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/bolt/')
        else:
            print(form.errors)
    return render(request, 'pages/add_shelter.html', {'form':form})
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def add_animal(request):
    if request.method == 'POST':
        try:
            result_post = json.loads(request.body)
        except:
            result_post = request.POST
        systemDict = {}
        for key in result_post:
            systemDict[key] = result_post.get(key)
        name=request.FILES['picture'].name
        with open(os.path.join(BASE_DIR,'static','imgupload',name),'wb') as f:
            for i in request.FILES["picture"].chunks():
                f.write(i)
        Animal.objects.create(picture='/static/imgupload/'+name,**systemDict)
    return render(request, 'pages/shelter.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'bolt/register.html', context = {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})


def myaccount(request):
    userprofile = UserProfile.objects.get(username=request.session['username'])
    return render(request, "pages/myaccount2.html", {"userprofile":userprofile})


def fqa(request):
    form = FqaForm()
    if request.method == 'POST':
        form = FqaForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/bolt/')         
        else:
            print(form.errors)
    return render(request, 'pages/fqa.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if UserProfile.objects.filter(username=username):
            if UserProfile.objects.filter(username=username).first().password == password:
                request.session['username'] = username
                return redirect(reverse('bolt:index'))
            else:
                return render(request, 'pages/login.html', context={'data': 'user password error!'})
        else:
            return render(request, 'pages/login.html',context={'data': 'user not exist!'})
    else:
        return render(request, 'pages/login.html',context={'data': ''})


def user_logout(request):
    logout(request)
    return redirect(reverse('bolt:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
