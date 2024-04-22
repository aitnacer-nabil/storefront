from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Order, OrderItem

# Create your views here.
def say_hello(request):
    queryset = Product.objects.values('id','title','inventory','collection__title').filter(collection__title='Pets')[:10]
    queryset = OrderItem.objects.values('product_id').distinct()
    queryset = Product.objects.filter(id__in=queryset).values('id','title','inventory','collection__title').order_by('title')
    # Select Related (1)
    queryset = Product.objects.select_related('collection').filter(collection__title='Pets')[:10]
    # Prefetch Related (1)
    queryset = Order.objects.prefetch_related('customer').prefetch_related('orderitem__set').all().values('id','customer__first_name','customer__membership','orderitem__product__title').order_by('customer__first_name')
    queryset = Product.objects.filter(inventory__lt=10).order_by('title')
    queryset = Order.objects.filter(customer__membership=Customer.MEMBERSHIP_GOLD).order_by('placed_at')


    return render(request, 'hello.html', {'name': 'World', 'products': queryset})
def customer(request):
    try:
        customers = Customer.objects.filter(email__icontains='.com')
        product = Product.objects.filter(inventory__ls=10)
        order = Order.objects.filter(customer__id=1)
        order
        return render(request, 'hello.html', {'name': 'Customer List', 'products': customers})
    except ObjectDoesNotExist:
        return render(request, 'hello.html', {'name': 'World'})
    


