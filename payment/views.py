from django.shortcuts import render, redirect
from cart.cart import Cart
from store.models import Product
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User


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
        billing_form = PaymentForm()
    except ShippingAddress.DoesNotExist:
        shipping_instance = None

    if request.method == 'GET':
        if shipping_instance:
            form = ShippingForm(instance=shipping_instance)
            billing_form = PaymentForm()
        else:
            form = ShippingForm()
    else:
        form = ShippingForm(request.POST, instance=shipping_instance)
        billing_form = PaymentForm()
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

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

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

def payment_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        if request.user.is_authenticated:
            return render(request, 'payment_info.html', {
                "cart_products": cart_products,
                "totals": totals,
                "quantities": quantities,
                "billing_info": request.POST.dict()
            })
        else:
            messages.warning(request, "You must be logged in to proceed.")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to access that page")
        return redirect('home')

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = totals
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}\n"

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user = user, full_name=full_name, email=email, amount_paid=amount_paid, shipping_address=shipping_address)
            create_order.save()

            for item in cart_products:
                product = item['product']
                quantity = item['quantity']
                price = product.sale_price if product.is_sale else product.price

                OrderItem.objects.create(
                    order=create_order,
                    product=product,
                    user=request.user if request.user.is_authenticated else None,
                    quantity=quantity,
                    price=price
                )

            messages.success(request, "Order placed successfully")
            return redirect('home')
        else:
            create_order = Order(full_name=full_name, email=email, amount_paid=amount_paid,shipping_address=shipping_address)
            create_order.save()
            for item in cart_products:
                product = item['product']  # se è così
                quantity = item['quantity']
                price = product.sale_price if product.is_sale else product.price

                OrderItem.objects.create(
                    order=create_order,
                    product=product,
                    user=request.user if request.user.is_authenticated else None,
                    quantity=quantity,
                    price=price
                )
            messages.success(request, "Order placed successfully")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to access that page")
        return redirect('home')