from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import ProductCategories, Products
from django.template import loader


def index(request):
    return render(request, 'library/index.html')


def search(request):
    query = request.GET.get('query')
    if not query:
        products = Products.objects.all()
    else:
        products = Products.objects.filter(name_product__icontains=query)

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
