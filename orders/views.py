from django.shortcuts import redirect, render
from django.http import HttpResponse

from carts.models import CartItem
from orders.models import Order
from .forms import OrderForm

# Create your views here.
def place_order(request,total = 0,quantity = 0):
    current_user = request.user
    
    cart_items = CartItem.objects.get(user = current_user)
    cart_count = cart_items.count()
    
    if cart_count == 0:
        return redirect("store:store")
    
    grand_total,tax = 0,0
    
    for cart_item in cart_items:
        total+=(cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (2*total)/100
    grand_total = total+tax
    
    if request.method == "POST":
        form = OrderForm(request.POST) 
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data('first_name')
            data.last_name = form.cleaned_data('last_name')
            data.phone = form.cleaned_data('phone')
            data.email = form.cleaned_data('email')
            data.address_line_1 = form.cleaned_data('address_line_1')
            data.address_line_2 = form.cleaned_data('address_line_2')
            data.state = form.cleaned_data('state')
            data.city = form.cleaned_data('city')
            data.order_note = form.cleaned_data('order_note')
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
