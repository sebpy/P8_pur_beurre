from django.shortcuts import render, get_object_or_404

from .models import ProductCategories, Products
from django.template import loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template('library/index.html')
    return HttpResponse(template.render(request=request))


def search(request):
    query = request.GET.get('search')
    if not query:
        products = Products.objects.all()
    else:
        # title contains the query and query is not sensitive to case.
        products = Products.objects.filter(name_product__icontains=query)


    products = ["<li>{}</li>".format(product.name_product) for product in products]
    message = """
            Nous avons trouvé les albums correspondant à votre requête ! Les voici :
            <ul>{}</ul>
        """.format("</li><li>".join(products))

    return HttpResponse(message)

def search(request):
    query = request.GET.get('search')
    if not query:
        products = Products.objects.all()
    else:
        products = Products.objects.filter(name_product__icontains=query)

    context = {
        'name_product': products,
    }
    return render(request, 'library/search.html', locals())
