from django.shortcuts import render

def static_page(page):
    """Renders static templates"""
    def handler(request):

        context = {
            'slug': page
        }
        
        return render(request, page + '.html', context)

    return handler

def index(request):


    # Testing many items
    products = []
    for i in range(20):
        products += [{
            'id': i,
            'title': f'Test{i}',
            'price': i*20
        }]
    
    context = {
        'slug': 'index',
        'products': products
    }

    return render(request, 'index.html', context)
