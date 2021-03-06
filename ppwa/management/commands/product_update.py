from __future__ import print_function

import os
import logging

from django.core.management.base import BaseCommand, CommandError
from django import db
from django.conf import settings

from ...models import Product
from ... import api

logger = logging.getLogger('ppwa.command')


class Command(BaseCommand):
    help = '''Update local product list from product API.'''

    def add_arguments(self, parser):
        parser.add_argument('--auth', help='first.last', default=os.environ.get('PPWA_AUTH', settings.PRODUCT_API_AUTH))
        parser.add_argument('--url', help='''Product list API URL.''', default=settings.PRODUCT_API_URL)

    def handle(self, *args, **options):
        if options['auth'] is None:
            raise CommandError('''first.last authentication must be provided on command line or Environment variable "PPWA_AUTH".''')
        products = self._get_product_list(options['auth'], options['url'])
        new, up, old = self._persist_product_list(products)
        return '''%i records: %i new, %i updated. %i products deprecated.''' % (new + up, new, up, old)

    def _get_product_list(self, auth, url):
        '''
        API returns {count, results}.

        :param auth: XAUTH string.
        :param url: URL of product listing API.
        :return: list of dictionaries {id, uuid, slug, name}.
        '''
        try:
            data = api.product_list()
            if 'results' not in data or 'count' not in data:
                logger.debug(str(data))
                raise ValueError('''Malformed JSON''')
            logger.debug('Recieved %i products from api' % (data['count'], ))
            return data['results']
        except ValueError as e:
            logger.error(e)
            raise CommandError(e)
        except api.HTTPError as e:
            raise CommandError('''HTTP error: %s''' % e)

    @db.transaction.atomic
    def _persist_product_list(self, products):
        '''Persist product list data to local storage.

        Key off of product uuid field.

        Two transaction wrapped steps:
          1. Add/Update products and timestamp.
          2. Mark inactive products with date_updated < timestap.

        :param products: list of dictionaries {id, uuid, slug, name}.
        :return: (new products added, existing products updated, existing products no longer available)
        '''
        # Reads/writes O(n), reads could be O(1).
        timestamp = Product.utcnow()
        new = 0
        updated = 0
        for data in products:
            try:
                product = Product.objects.get(uuid=data['uuid'])
                # API is source of truth. If we differ, we are wrong.
                if product.id != data['id']:
                    product.delete()
                    raise Product.DoesNotExist
                updated += 1
            except Product.DoesNotExist:
                product = Product(uuid=data['uuid'])
                product.id = data['id']
                new += 1
            product.name = data['name']
            product.slug = data['slug']
            product.is_active = True
            product.date_updated = timestamp
            product.save()
        old = Product.objects.filter(date_updated__lt=timestamp).update(is_active=False)
        logger.info('Persisted %i new, %i updated, and %i inactive products' % (new, updated, old, ))
        return new, updated, old
