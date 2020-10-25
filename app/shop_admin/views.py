import base64
import os
from shutil import copy, rmtree

from django.conf import settings
from django.shortcuts import render
from shop.models import Category, Product
from django.http import HttpResponse, Http404
from rest_framework.parsers import JSONParser

from .serializers import ProductSerializer, CategorySerializer

def shop_admin(request):
    validation = validate(request)
    if(validation != True):
        return validation

    context = {
        'categories': Category.objects.all(),
        'products': Product.objects.all()
    }

    return render(request, 'admin_index.html', context) 

# :FIXME: Split categories and products methods

##############
# Categories #
##############

def admin_category(request, id):
    validation = validate(request)
    if(validation != True):
        return validation

    if id != 'new':
        context = {
            'cat': Category.objects.get(id = int(id))
        }
    else:
        context = {
            'new': True
        }

    return render(request, 'admin_category.html', context)

def admin_edit_category(request):
    validation = validate(request)
    if(validation != True):
        return validation

    if(request.method != 'POST'):
        raise Http404('No such method')

    category = None
    if request.POST['id'] != 'new':
        category = Category.objects.get(id = int(request.POST['id']))
        
    serializer = CategorySerializer(category, data = request.POST)

    if not serializer.is_valid():
        raise Http402('Invalid product object')
    
    serializer.save()
    
    return HttpResponse(serializer.data['id'])

def admin_delete_category(request):
    validation = validate(request)
    if(validation != True):
        return validation

    if(request.method != 'POST'):
        raise Http404('No such method')
    
    cat = Category.objects.get(id=request.POST['id'])
    for pr in cat.product_set.all():
        rmtree(os.path.join(setting.MEDIA_ROOT, str(pr.id)))
        cat.delete()
    return HttpResponse()

############
# Products #
############

def admin_edit(request):
    validation = validate(request)
    if(validation != True):
        return validation

    if(request.method != 'POST'):
        raise Http404('No such method')

    pr = None
    if request.POST['id'] != 'new':
        pr = Product.objects.get(id = int(request.POST['id']))
        
    serializer = ProductSerializer(pr, data = request.POST)

    if not serializer.is_valid():
        response = HttpResponse('Invalid product object')
        response.status_code = 400
        return response
    serializer.save()

    if request.POST['id'] == 'new':
        os.mkdir(os.path.join(settings.MEDIA_ROOT, str(serializer.data['id'])))
        copy(
            os.path.join(
                settings.STATIC_ROOT,
                'img',
                'noimg.jpg'),
            os.path.join(
                settings.MEDIA_ROOT,
                str(serializer.data['id']),
                '0.jpg')
        )
    
    return HttpResponse(serializer.data['id'])

def admin_product(request, id):
    validation = validate(request)
    if(validation != True):
        return validation

    if id != 'new':
        context = {
            'pr': Product.objects.get(id = id),
        }
    else:
        context = {
            'new': True
        }
    context['categories'] = Category.objects.all()
    return render(request, 'admin_product.html', context)

def admin_image(request):
    validation = validate(request)
    if(validation != True):
        return validation
    
    if(request.method == "POST"):
        pr = Product.objects.get(id=request.POST['id'])
        i = pr.img_cnt
        if(request.POST['replace'] == 'true'):
            if len(request.FILES.getlist('files')) != 1:
                response = HttpResponse('Wrong count of files to replace')
                response.status_code = 400
                return response
            handle_uploaded_file(file, pr.id, int(request.POST['replace_id']))
        for file in request.FILES.getlist('files'):
            handle_uploaded_file(file, pr.id, i)
            i += 1
        pr.img_cnt = i
        pr.save()
    return HttpResponse('')


def admin_delete(request):
    validation = validate(request)
    if(validation != True):
        return validation

    pr = Product.objects.get(id=int(request.GET['id']))
    rmtree(os.path.join(settings.MEDIA_ROOT, str(pr.id)))
    pr.delete()
    return HttpResponse('new')

def handle_uploaded_file(f, pr_id, id):
    with open(os.path.join(settings.MEDIA_ROOT, str(pr_id), str(id) + '.jpg'), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def validate(request):
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % "Basci Auth Protected"
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if(len(auth) == 2):
            if auth[0].lower() == 'basic':
                user, password = base64.b64decode(auth[1]).decode().split(':')
                if password == os.environ.get('ADMIN_PASS', ''):
                    return True
    return response
