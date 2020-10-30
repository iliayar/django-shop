from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Product, Category

def static_page(page):
    """Renders static templates"""
    def handler(request):

        context = {
            'slug': page,
            'categories': Category.objects.all()
        }
        
        return render(request, page + '.html', context)

    return handler

def index(request):
    """Starting page"""
    
    categories = Category.objects.all()

    if(len(categories) == 0):
        context = {
            'slug': 'index',
            'categories': []
        }
        return render(request, 'index.html', context)
    
    return HttpResponseRedirect(reverse(category, kwargs={'id': categories[0].id}))

def category(request, id):
    """Category view, display all products in category.
       Empty page if there are no any categories"""
    cat = Category.objects.get(id = id)
    
    context = {
        'slug': cat.id,
        'products': cat.product_set.all(),
        'categories': Category.objects.all(),
        'cat': cat
    }

    return render(request, 'index.html', context)
    

def product(request, id):
    """Product view, displays product information"""
    pr = Product.objects.get(id = id)
    cat = pr.category
    
    context = {
        'slug': cat.id,
        'pr': pr,
        'categories': Category.objects.all(),
        'cat': cat,
        'images': [0] if pr.img_cnt == 0 else list(range(pr.img_cnt))
    }

    return render(request, 'product.html', context)
