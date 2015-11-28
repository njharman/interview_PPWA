import base64
import logging

from django import forms
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.list import MultipleObjectMixin

from .models import Product, Customer, Order
from . import api

logger = logging.getLogger('ppwa.view')


def _encode_confirmation(quantity, confirmation):
    '''urlsafe encode quantity, confirmation'''
    # TODO: Verify assumption that confirmation code will never contain '+' (or escape it).
    return base64.urlsafe_b64encode('%s+%s' % (quantity, confirmation))


def _decode_confirmation(code):
    '''undo _encode_confirmation() and return quantity, confirmation'''
    data = base64.urlsafe_b64decode(str(code))
    quantity, confirmation = data.split('+')
    return quantity, confirmation


class PurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)  # TODO: max_value
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()

    def clean_name(self):
        data = self.cleaned_data['name']
        # TODO: Stinks that "default value" logic is spread between here and html.
        if 'your name' == data:
            raise forms.ValidationError('Please enter your name.')
        return data

    def clean_phone(self):
        # TODO: Validate value looks like phone number?
        data = self.cleaned_data['phone']
        # TODO: Stinks that "default value" logic is spread between here and html.
        if 'phone' == data:
            raise forms.ValidationError('Please enter your phone number.')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        # TODO: Stinks that "default value" logic is spread between here and html.
        if 'email' == data:
            raise forms.ValidationError('Please enter your email address.')
        return data


class ProductList(ListView, MultipleObjectMixin):
    '''Paginated list of Products.'''
    queryset = Product.objects.filter(is_active=True)
    context_object_name = 'products'
    paginate_by = 10
    paginate_orphans = 5


class ProductDetail(FormView, DetailView):
    '''Display product details, POST to purchase product.'''
    model = Product
    form_class = PurchaseForm

    # TODO: Bastardidation of these attributes.
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def _product(self):
        uuid = self.request.resolver_match.kwargs['uuid']  # TODO: Really best way to get uuid?
        return Product.objects.get(uuid=uuid)

    def form_valid(self, form):
        logger.debug('valid purchase form')
        product = self._product()
        quantity = form.cleaned_data['quantity']
        cust_name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        try:
            api_response = api.post_purchase(product.id, quantity, cust_name=cust_name, email=email, phone=phone)
        except ValueError:
            logger.error('Purchase API JSON parsing error.')
        except api.HTTPError:
            logger.error('Purchase API HTTP error.')
        logger.debug('Purchase API response:' + str(api_response))
        if api_response and 'confirmation_code' in api_response:
            quantity = api_response['quantity']  # overwrite submitted quantity in case api says less.
            confirmation = api_response['confirmation_code']
            # TODO: api returns user_id, probably should be stored in Customer.
            customer, created = Customer.objects.get_or_create(name=cust_name, email=email, phone=phone)
            order = Order(customer=customer, product=product, product_name=product.name, price=product.price, quantity=quantity, confirmation=confirmation)
            order.save()
        else:
            quantity = 0
            confirmation = ''
        # Encode data for thank you page.
        # TODO: With users / sessions this would better be handled in redis/memcache/datatable/DJsessions.
        code = _encode_confirmation(quantity, confirmation)
        return redirect('purchase-confirmation', uuid=product.uuid, code=code)
        # return super(ProductDetail, self).form_valid(form)

    def form_invalid(self, form):
        logger.debug('invalid purchase form')
        self.object = self._product()  # DetailView expects self.object to be set.
        response = super(ProductDetail, self).form_invalid(form)
        return response


class PurchaseConfirmation(TemplateView):
    '''Display "thank you" or "sorry" page post purchase.'''
    template_name = 'ppwa/purchase_thankyou.html'

    def get_context_data(self, **kwargs):
        context = super(PurchaseConfirmation, self).get_context_data(**kwargs)
        quantity, confirmation = _decode_confirmation(self.request.resolver_match.kwargs['code'])
        if quantity != '0':
            uuid = self.request.resolver_match.kwargs['uuid']  # TODO: Really best way to get uuid?
            product = Product.objects.get(uuid=uuid)
            context['purchase'] = True
            context['name'] = product.name
            context['quantity'] = quantity
            context['confirmation'] = confirmation
        return context
