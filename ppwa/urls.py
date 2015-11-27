from django.conf.urls import include, url

from .views import ProductList, ProductDetail

urlpatterns = [
    # TODO: Use slug for product detail? Guarantee of uniqueness?
    url(r'^(?P<uuid>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})/$', ProductDetail.as_view(), name='product-detail'),
    url(r'^$', ProductList.as_view(), name='product-list'),
    ]
