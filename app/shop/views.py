from django.shortcuts import render

def static_page(page):

    def handler(request):

        context = {
            'slug': page
        }
        
        return render(request, page + '.html', context)

    return handler
