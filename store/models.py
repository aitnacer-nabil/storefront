from django.db import models


# user 1 - * Cart ??
# user 1 - *  order done 
# order 1 - * order_items  done 
# cart 1 -* cart_item done
# cart_item 1 - * product done 
# order_items 1 - * product done
# Promotion * - * Product
# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    feature_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name="+"
    )


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_At = models.DateTimeField(auto_now=True)
    inventory = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='B')


class Order(models.Model):
    PENDING = 'p'
    COMPLETE = 'c'
    FAILED = 'f'
    PAYMENT_STATUS = [
        (PENDING, 'Pending'),
        (FAILED, 'Failed'),
        (COMPLETE, 'Complete')
    ]
    placed_at = models.DateField(auto_now=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_prive = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
