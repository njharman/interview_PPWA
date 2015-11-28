''' End-to-end tests. Hitting API, database, etc.
'''
import unittest

from django.test import TestCase, Client
from django.core.urlresolvers import reverse


from . import api
from . import models


class APITestCase(TestCase):
    # TODO: test malformed json exception handling

    def test_product_list(self):
        data = api.product_list()
        self.assertTrue('count' in data)
        self.assertTrue('results' in data)

    def test_product_detail(self):
        expected = ['id', 'name', 'uuid', 'slug', 'price', 'cost', 'inventory_on_hand', 'description', ]
        data = api.product_detail(106)  # 106 is(was?) known product id.
        for key in expected:
            self.assertTrue(key in data)

    def test_product_detail_fail(self):
        pid = 999349399399  # Guessing no product with this id.
        self.assertRaises(api.HTTPError, api.product_detail, pid)

    @unittest.skip('''TBD - pain to test.''')
    def test_product_purchase_fail(self):
        pass
        # iterate over products find one with no inventory
        #   assert It post fails.

    @unittest.skip('''TBD - pain to test.''')
    def test_product_purchase_success(self):
        pass
        # iterate over products find one with inventory
        #   assert post works.


class ModelsTestCase(TestCase):
    def test_Product_properties(self):
        expected = ['id', 'name', 'uuid', 'slug', 'price', 'cost', 'inventory_on_hand', 'description', ]
        # 106 is assumed to be existing product.
        t = models.Product(id=106, name='name', slug='slug', uuid='6be7a269-0f14-4a53-b740-0e82cb1c1e6a', is_active=True, date_updated=models.Product.utcnow())
        self.assertFalse(hasattr(t, '_detail_cache'))
        t.price  # Property that causes api call.
        self.assertTrue(hasattr(t, '_detail_cache'))
        for key in expected:
            self.assertTrue(key in t._detail)
        t.inventory
        t.description


class ViewsTestCase(TestCase):
    def setUp(self):
        # Populate product db.
        p = models.Product(id=106, name='name', slug='slug', uuid='4e902117-f0a4-4850-9cca-a81725367e70', is_active=True, date_updated=models.Product.utcnow())
        p.save()

    def test_product_list(self):
        c = Client()
        response = c.get(reverse('product-list'))
        self.assertTrue('products' in response.context)

    def test_product_detail(self):
        c = Client()
        kwargs = {'uuid': '4e902117-f0a4-4850-9cca-a81725367e70', }
        response = c.get(reverse('product-detail', kwargs=kwargs))
        self.assertTrue('product' in response.context)

    @unittest.skip('''TBD - pain to test.''')
    def test_purchase(self):
        c = Client()
        kwargs = {'uuid': '4e902117-f0a4-4850-9cca-a81725367e70', }
        response = c.post(reverse('product-purchase', kwargs=kwargs))

    def test_purchase_confirmation(self):
        c = Client()
        kwargs = {
                'uuid': '4e902117-f0a4-4850-9cca-a81725367e70',
                'code': 'MysyMzQzMjQ=',  # result of view._encode_confirmation(3,234324)
                }
        response = c.get(reverse('purchase-confirmation', kwargs=kwargs))
        self.assertEqual('3', response.context['quantity'])
        self.assertEqual('234324', response.context['confirmation'])

    def test_purchase_sorry(self):
        c = Client()
        kwargs = {
                'uuid': '4e902117-f0a4-4850-9cca-a81725367e70',
                'code': 'MCs=',  # result of view._encode_confirmation(0,'')
                }
        response = c.get(reverse('purchase-confirmation', kwargs=kwargs))
        self.assertFalse('purchase' in response.context)
        self.assertFalse('quantity' in response.context)
        self.assertFalse('confirmation' in response.context)
