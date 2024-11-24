from datetime import date, timedelta
from itertools import product

from django.core.mail import send_mail
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from pyexpat.errors import messages

from app_user.models import Customer
from .models import Product, Cart, CartItem, Category


class CategoryView(ListView):
    model = Category
    template_name = 'app_product/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        search = self.request.GET.get('q', '')

        if search:
            return Category.objects.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        else:
            return Category.objects.all()


class ProductView(ListView):
    model = Product
    template_name = 'app_main/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        search = self.request.GET.get('q', '')
        category_id = self.kwargs.get('category_id')

        if search:
            return Product.objects.filter(
                Q(title__icontains=search) | Q(description__icontains=search) | Q(category__title__icontains=search)
            )
        else:
            return Product.objects.filter(category__id=category_id)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_product/product_detail.html'
    context_object_name = 'product'


def cart(request):
    return render(request, 'app_product/cart.html')


def checkout(request):
    cart = request.session.get('cart', {})

    email = request.user.email
    if request.user.is_authenticated :
        product_details = []
        total_amount = 0

        for product_id, details in cart.items():
            product_name = details.get('name')
            quantity = details.get('quantity', 0)
            price = details.get('new_price', 0)
            total_price = price * quantity
            product_details.append(f"{product_name} - Quantity: {quantity}, Total: ${total_price}")
            total_amount += total_price

        shipping_cost = 10
        total_amount_with_shipping = total_amount + shipping_cost

        message = "\n".join(product_details)
        message += f"\n\nSubtotal: ${total_amount}\nShipping: ${shipping_cost}\nTotal Amount: ${total_amount_with_shipping}"

        send_mail(
            subject="Order Confirmation",
            message=message,
            from_email="odiloffr@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        request.session['cart'] = {}
        messages.success(request, "Your order has been placed successfully!")

        return redirect('home')
    else:
        return redirect('home')


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        total_price = sum(item.product.new_price * item.quantity for item in cart_items)

        return render(request, 'app_main/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            '10_day': date.today() + timedelta(days=10),
            'today': date.today(),
            'total_all': total_price + 10
        })
    else:
        messages.info(request, 'you should be logged in')
        return redirect('login')


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.info(request, 'you should login first')
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        product=product, user=request.user,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, product_id=product_id, user=request.user)

    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart_view')


def change_product_cart(request, product_id, action):
    cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user)

    if action == 'increment':
        cart_item.quantity += 1

    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        elif cart_item.quantity == 1:
            cart_item.delete()
            return redirect('cart_view')

    cart_item.save()

    return redirect('cart_view')


def checkout(request):
    cart = request.session.get('cart', {})

    email = request.user.email
    if request.user.is_authenticated :
        product_details = []
        total_amount = 0

        for product_id, details in cart.items():
            product_name = details.get('name')
            quantity = details.get('quantity', 0)
            price = details.get('new_price', 0)
            total_price = price * quantity
            product_details.append(f"{product_name} - Quantity: {quantity}, Total: ${total_price}")
            total_amount += total_price

        shipping_cost = 10
        total_amount_with_shipping = total_amount + shipping_cost

        message = "\n".join(product_details)
        message += f"\n\nSubtotal: ${total_amount}\nShipping: ${shipping_cost}\nTotal Amount: ${total_amount_with_shipping}"

        send_mail(
            subject="Order Confirmation",
            message=message,
            from_email="asad2001psabirov@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        request.session['cart'] = {}
        messages.success(request, "Your order has been placed successfully!")

        return redirect('home')
    else:
        return redirect('home')


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        total_price = sum(item.product.new_price * item.quantity for item in cart_items)

        return render(request, 'app_product/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            '10_day': date.today() + timedelta(days=10),
            'today': date.today(),
            'total_all': total_price + 10
        })
    else:
        messages.info(request, 'you should be logged in')
        return redirect('login')

