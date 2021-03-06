from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import UserProfile
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime


#def angel(request):
#    return render(request, 'index.html', {})


def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context_dict)
    return response


def about(request):
    # if request.session.test_cookie_worked():
    #    print("TEST COOKIE WORKED!")
    #    request.session.delete_test_cookie()
    context_dict = {'boldmessage': "This is about page"}
    print(request.method)
    print(request.user)

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()
    # HHTP post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)
            # Direct the user back to the index page
            return index(request)
        else:
            # Print errors to terminal
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(
        request, 'last_visit', str(datetime.now()))
    
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 1:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def track_url(request):
    url = '/rango/'

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            
            page = Page.objects.get(id=page_id)
            page.views+= 1
            url = page.url
            page.save()

    return redirect(url)


@login_required
def register_profile(request):
    #user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)#, instance = user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)
    
    context_dict = {'form': form}

    return render(request, 'registration/profile_registration.html', context_dict)
    

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except user.DoesNotExist:
        redirect('index')

    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({
        'website': user_profile.website, 
        'picture': user_profile.picture
    })

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance = user_profile)
        if form.is_valid():
            form.save(commit=True)
        else:
            print(form.errors)
    
    context_dict = {
        'form': form, 
        'user_profile': user_profile, 
        'selecteduser': user
    }

    return render(request, 'registration/profile.html', context_dict)


@login_required
def profiles_list(request):
    profiles = UserProfile.objects.all()

    context_dict = {'profiles': profiles}

    return render(request, 'registration/profiles_list.html', context_dict)

