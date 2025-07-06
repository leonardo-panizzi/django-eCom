from django.shortcuts import render, redirect
from cart.cart import Cart
from store.models import Product
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib import messages


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    totals = cart.cart_total()
    product_ids = cart.cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    quantities = {str(p.id): cart.cart[str(p.id)]['quantity'] for p in products}

    try:
        shipping_instance = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_instance = None

        # Inizializza il form
    if request.method == 'GET':
        if shipping_instance:
            form = ShippingForm(instance=shipping_instance)
        else:
            form = ShippingForm()
    else:
        form = ShippingForm(request.POST, instance=shipping_instance)

    return render(request, 'payment/checkout.html', {
        'cart_products': products,
        'quantities': quantities,
        'totals': totals,
        'shipping_form': form,
    })

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        if request.user.is_authenticated:
            return render(request, 'billing_info.html', {
                "cart_products": cart_products,
                "totals": totals,
                "quantities": quantities,
                "shipping_info": request.POST.dict()
            })
        else:
            messages.warning(request, "You must be logged in to proceed.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to access that page")
        return redirect('home')