from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

#def angel(request):
#    return render(request, 'index.html', {})

def index(request):
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'boldmessage': "This is about page"}
    return render(request, 'rango/about.html', context=context_dict)
