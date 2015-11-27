import logging

from django.db import models

from . import api

logger = logging.getLogger('wwpa.model')


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=60)
    uuid = models.UUIDField(db_index=True)
    is_active = models.BooleanField(default=True, help_text='''Set false if product no longer "carried".''')
    date_updated = models.DateTimeField(help_text='''Set by data updater.''')

    def __unicode__(self):
        return self.slug

    @property
    def _detail(self):
        '''Dynamically pull detail info from product API.'''
        if not hasattr(self, '__detail'):
            # TODO: This latency / dependency sucks. Want current data. Assumption
            # that lifetime of this object is current enough.
            self.__detail = api.product_detail(self.id)
        return self.__detail

    @property
    def price(self):
        return self._detail['price']

    @property
    def description(self):
        return self._detail['description']

    @property
    def inventory(self):
        return self._detail['inventory_on_hand']


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    product_name = models.CharField(max_length=255)  # TODO: listed requirment, denormal with Product.name?
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='''Price at time of purchase.''')
    quantity = models.PositiveIntegerField(help_text='''Quantity Ordered.''')
    confirmation = models.CharField(max_length=255, help_text='''Confirmation code from purchase API.''')

    def __unicode__(self):
        return '%ix %s' % (self.quantity, self.product)
