from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=60)
    uuid = models.UUIDField(db_index=True)
    is_active = models.BooleanField(default=True, help_text='''Set false if product no longer "carried".''')
    date_updated = models.DateTimeField(help_text='''Set by data updater.''')

    def __str__(self):
        return self.slug


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    product_name = models.CharField(max_length=255)  # TODO: listed requirment, denormal with Product.name?
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='''Price at time of purchase.''')
    quantity = models.PositiveIntegerField(help_text='''Quantity Ordered.''')
    confirmation = models.CharField(max_length=255, help_text='''Confirmation code from purchase API.''')

    def __str__(self):
        return '%ix %s' % (self.quantity, self.product)
