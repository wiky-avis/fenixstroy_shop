from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from .forms import OrderCreateForm
from .models import Order, OrderItem
from django.core.mail import send_mail


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(
            request.POST or None, files=request.FILES or None)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                    )
            cart.clear()
            return render(
                request, 'orders/order/created.html', {'order': order}
                )
    else:
        form = OrderCreateForm
    return render(
        request, 'orders/order/create.html', {'cart': cart, 'form': form}
        )
