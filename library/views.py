from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Product
from .forms import LoginForm, RegisterForm


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

    query = request.GET.get('query', '')
    if not query:
        messages.error(request, '<strong><i class="fas fa-exclamation-triangle"></i> ERREUR!</strong><br>'
                                'Vous devez entrer un aliment à rechercher.', extra_tags='safe')

        return render(request, 'library/index.html')

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


def login_page(request):
    form_login = LoginForm()
    context = {
        "formLogin": form_login,
    }
    return render(request, 'library/login.html', context)


def login_user(request):
    form_login = LoginForm()
    context = {
        "formLogin": form_login,
    }

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, '<strong><i class="fas fa-exclamation-triangle"></i> Succès!</strong><br>'
                                          'Vous êtes connecté avec succès.', extra_tags='safe')

                return render(request, 'library/profile.html')

            else:
                messages.error(request, '<strong><i class="fas fa-exclamation-triangle"></i> Erreur!</strong><br>'
                                        'Login ou mot de passe invalide.', extra_tags='safe')

                return render(request, 'library/login.html', context)
    else:
        return render(request, 'library/login.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, '<strong><i class="fas fa-exclamation-triangle"></i> Succès!</strong><br>'
                              'Vous avez été déconnecté avec succès.', extra_tags='safe')

    return render(request, 'library/index.html')


def profile(request):
    return render(request, 'library/profile.html')


def register(request):
    form_register = RegisterForm()
    context = {
        "formRegister": form_register
    }
    try:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                email = form.cleaned_data.get('email')
                if password2 != password1:
                    messages.error(request, '<strong><i class="fas fa-exclamation-triangle"></i> Erreur!</strong><br>'
                                            'Les mot de passe sont différent', extra_tags='safe')
                else:
                    user = User.objects.create_user(username=username,
                                                    email=email,
                                                    password=password1)

                    User.objects.create(user=user)
                    user = authenticate(request, username=username, password=password1)
                    if user:
                        login(request, user)

                        return render(request, 'library/profile.html')
                    else:
                        messages.error(request, '<strong><i class="fas fa-exclamation-triangle"></i> Erreur!</strong><br>'
                                                'Vous devez remplir tous les champs.', extra_tags='safe')

        else:
            return render(request, 'library/register.html', context)

    except IntegrityError:
        messages.error(request, '<strong><i class="fas fa-exclamation-triangle"></i> Erreur!</strong><br>'
                                'Cette utilisateur existe déjà.', extra_tags='safe')

        return render(request, 'library/register.html', context)

    return render(request, 'library/register.html', context)
