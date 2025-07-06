from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.cart import Cart
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    product_ids = cart.cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    quantities = {str(p.id): cart.cart[str(p.id)]['quantity'] for p in products}
    # for product_id, item in cart.cart.items():
    #     product = get_object_or_404(Product, id=product_id)
    #     product.quantity = item.get('quantity', 1)
    #     product.subtotal = float(item.get('price')) * product.quantity
    #     cart_products.append(product)
    #
    # totals = sum(p.subtotal for p in cart_products)
    #
    # context = {
    #     'cart_products': cart_products,
    #     'totals': totals,
    # }
    context = {
        'cart_products': products,
        'totals': cart.cart_total(),
        'quantities': quantities,
    }
    return render(request, 'cart_summary.html', context)



def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=quantity)
        cart_quantity = cart.__len__()

        return JsonResponse({'qty': cart_quantity})


def cart_update(request):
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))  # prende id prodotto da POST
        product_qty = int(request.POST.get('product_qty'))  # prende quantità da POST

        cart = Cart(request)
        cart.update(product=product_id, quantity=product_qty)

        messages.success(request, "Cart updated")
        return JsonResponse({'message': 'Cart updated'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_delete(request):
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart = Cart(request)
        cart.delete(product=product_id)

        messages.success(request, "Product removed from cart")
        return redirect('cart_summary')
