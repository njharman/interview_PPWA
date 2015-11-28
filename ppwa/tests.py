import datetime
from unittest import TestCase

import pytz
from django.test import TestCase as DJTestCase


from .models import Product, Customer, Order
from .views import _encode_confirmation, _decode_confirmation


class FunctionTestCase(TestCase):
    def test_confirmation_encode(self):
        tests = [
                (None, None),
                (0, ''),
                # ('3', '/?+'),  # '+' is used as seperator.
                ('3', '/?'),
                (-1, '3cdmp3'),
                ]
        for a, b in tests:
            code = _encode_confirmation(a, b)
            a_, b_ = _decode_confirmation(code)
            # By design _decode returns strings.
            self.assertEqual(str(a), a_)
            self.assertEqual(str(b), b_)

    def test_decode_unicode(self):
        # Django gives unicode, base64 no like it.
        code = _encode_confirmation(0, u'23423')
        a, b = _decode_confirmation(unicode(code))
        self.assertEqual('0', a)
        self.assertEqual('23423', b)


class ProductModelTestCase(DJTestCase):
    def test_basic(self):
        t = Product(name='name', slug='slug', uuid='6be7a269-0f14-4a53-b740-0e82cb1c1e6a', is_active=True, date_updated=Product.utcnow())
        self.assertEqual('slug', str(t))
        self.assertEqual(u'slug', unicode(t))
        # TODO: mock api and access properties.
        t.save()

    def test_utcnow(self):
        expected = datetime.datetime.utcnow()
        t = Product.utcnow()
        self.assertEqual(pytz.utc, t.tzinfo)
        self.assertEqual(expected.year, t.year)
        self.assertEqual(expected.month, t.month)
        self.assertEqual(expected.day, t.day)
        self.assertEqual(expected.hour, t.hour)
        self.assertEqual(expected.minute, t.minute)
        self.assertEqual(expected.second, t.second)
        # If all that worked, assume microseconds did too...


class CustomerModelTestCase(DJTestCase):
    def test_basic(self):
        t = Customer(name='name', phone='phone', email='email')
        self.assertEqual('name', str(t))
        self.assertEqual(u'name', unicode(t))
        t.save()

    def test_maxlength(self):
        # name 100 chars
        # phone 25 chars
        Customer(name='a' * 101, phone='123-456-7890', email='email').save()
        Customer(name='name', phone='1' * 26, email='email').save()

    def test_uniqueness(self):
        t1 = Customer(name='name', phone='phone', email='email')
        t1.save()
        t2 = Customer(name='name', phone='phone', email='email')
        t2.save()


class OrderModelTestCase(DJTestCase):
    def test_basic(self):
        c = Customer(name='name', phone='phone', email='email')
        c.save()
        p = Product(name='product', slug='slug', uuid='6be7a269-0f14-4a53-b740-0e82cb1c1e6a', is_active=True, date_updated=Product.utcnow())
        p.save()
        t = Order(customer=c, product=p, product_name='product_name', price=22.0, quantity=3, confirmation='confirmation')
        self.assertEqual('3x product_name', str(t))
        self.assertEqual(u'3x product_name', unicode(t))
        t.save()
