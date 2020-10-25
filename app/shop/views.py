from django.shortcuts import render
from .models import Product

def static_page(page):
    """Renders static templates"""
    def handler(request):

        context = {
            'slug': page
        }
        
        return render(request, page + '.html', context)

    return handler

def index(request):


    context = {
        'slug': 'index',
        'products': Product.objects.all()
    }

    return render(request, 'index.html', context)
