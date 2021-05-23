from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total' : 0,
            'get_cart_items' : 0,
            'shipping' : False
        }
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context={ 
        'products' : products,
        'cartItems' : cartItems
        }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total' : 0,
            'get_cart_items' : 0,
            'shipping' : False 
        }
        cartItems = order['get_cart_items']
    context={
        'items' : items,
        'order': order,
        'cartItems' : cartItems
        }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total' : 0,
            'get_cart_items' : 0,
            'shipping' : False
        }
        cartItems = order['get_cart_items']
    context={
        'items': items,
        'order' : order,
        'cartItems' : cartItems
    }
    return render(request, "store/checkout.html", context)

def updateItem(request):
    data =json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action: ',action)
    print('productId: ',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quatity = (orderItem.quatity + 1)
    elif action == 'remove':
        orderItem.quatity = (orderItem.quatity - 1)

    orderItem.save()

    if orderItem.quatity <=0:
        orderItem.delete
    return JsonResponse('Item Added', safe=False)

def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data =json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete=True
        order.save()

        if order.shipping == True:
            ShippingAdress.objects.create(
                customer=customer,
                order=order,
                adress=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zip_code=data['shipping']['zipcode'],
            )
    
    else:
        print('user is not logged in...')
    return JsonResponse('payment complete', safe=False)