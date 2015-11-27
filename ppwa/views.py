import logging

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.list import MultipleObjectMixin

from .models import Product

logger = logging.getLogger('wwpa.view')


class ProductList(ListView, MultipleObjectMixin):
    queryset = Product.objects.filter(is_active=True)
    context_object_name = 'products'
    paginate_by = 10
    paginate_orphans = 5


class ProductDetail(DetailView):
    model = Product

    # TODO: Bastardidation of these attributes.
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
