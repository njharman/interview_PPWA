import datetime
import logging

import pytz
from django.db import models

from . import api

logger = logging.getLogger('ppwa.model')


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
        # TODO: API/JSON/Network exceptions are an issue.
        if not hasattr(self, '_detail_cache'):
            # TODO: This latency / dependency sucks. Want current data. Assumption
            # that lifetime of Product instance is current enough.
            self._detail_cache = api.product_detail(self.id)
        return self._detail_cache

    @property
    def price(self):
        return self._detail['price']

    @property
    def description(self):
        return self._detail['description']

    @property
    def inventory(self):
        return self._detail['inventory_on_hand']

    @staticmethod  # Cause it's convinient to have this on Product.
    def utcnow():
        '''Python in its invinate wisdom does not add TZ to utcnow()'''
        return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=25)
    email = models.EmailField()

    class Meta:
        unique_together = (('name', 'phone', 'email'), )

    def __unicode__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer)
    # TODO: Link by uuid, cause update_products may change pk.
    product = models.ForeignKey(Product)
    product_name = models.CharField(max_length=255)  # TODO: listed requirment, denormal with Product.name?
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='''Price at time of purchase.''')
    quantity = models.PositiveIntegerField(help_text='''Quantity Ordered.''')
    confirmation = models.CharField(max_length=255, help_text='''Confirmation code from purchase API.''')

    def __unicode__(self):
        return '%ix %s' % (self.quantity, self.product_name)
