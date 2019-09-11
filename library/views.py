from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import ProductCategorie, Product
from django.template import loader


def index(request):
    return render(request, 'library/index.html')


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'name_product': product.name_product,
        'nutriscore_product': product.nutriscore_product,
        'fat_100g': product.fat_100g,
        'sugars_100g': product.sugars_100g,
        'saturated_fat_100g': product.saturated_fat_100g,
        'salt_100g': product.salt_100g,
        'image_product': product.image_product,
        'link_product': product.link_product
    }
    return render(request, 'library/detail.html', context)


def search(request):
    query = request.GET.get('query')
    if not query:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name_product__icontains=query)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'query': query,
        'paginate': True
    }
    return render(request, 'library/search.html', context)
