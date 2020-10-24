import base64
import os
from shutil import copy, rmtree

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

    data = JSONParser().parse(request)
    
    serializer = ProductSerializer(data = data)

    if not serializer.is_valid():
        raise Http402('Invalid product object')
    serializer.save()
    
    if(request.POST['id'] == 'new'):
        copy(
            os.path.join(
                settings.STATIC_ROOT,
                'img',
                'noimg.jpg'),
            os.path.join(
                settings.MEDIA_ROOT,
                str(serializer.data.id),
                '0.jpg')
        )
    return HttpResponse(serializer.data.id)

def admin_product(request, id):
    validation = validate(request)
    if(validation != True):
        return validation

    if id != 'new':
        context = {
            'pr': {
                'id': 0,
                'price': 1337,
                'title': 'Test',
                'description': 'Some description',
                'specification': {
                    'test_param': 'value',
                    'test_param_2': 'value_2'
                },
                'category': Category(id = 0)
            }
        }
    else:
        context = {
            'new': True
        }
    return render(request, 'admin_product.html', context)


# def admin_img(request):
#     if(request.method == "POST"):
#         pr = Product.objects.get(id=request.POST['id'])
#         i = pr.img_cnt
#         for file in request.FILES.getlist('files'):
#             if request.POST['replace'] == 'true':
#                 handle_uploaded_file(
#                     file, pr.title + '_' + str(request.POST['replace_id']))
#             else:
#                 handle_uploaded_file(file, pr.title + '_' + str(i))
#                 i += 1
#         pr.img_cnt = i
#         pr.save()
#     return HttpResponse('', RequestContext(request))


# def admin_delete(request):
#     validation = validate(request)
#     if(validation != True):
#         return validation

#     pr = Product.objects.get(id=request.GET['id'])
#     for file in glob(
#         os.path.join(
#             settings.STATIC_ROOT,
#             'img',
#             pr.title +
#             '_*')):
#         os.remove(file)
#     pr.delete()
#     return HttpResponse('new')

# def handle_uploaded_file(f, name):
#     with open(os.path.join(settings.STATIC_ROOT, 'img', name), 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def validate(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if(len(auth) == 2):
            if auth[0].lower() == 'basic':
                user, password = base64.b64decode(auth[1]).decode().split(':')
                if password == os.environ.get('ADMIN_PASS', ''):
                    return True
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % "Basci Auth Protected"
    return response
