from django.conf.urls import url

from .views import ProductList, ProductDetail, PurchaseConfirmation

urlpatterns = [
    # TODO: Use slug for product detail? Guarantee of uniqueness?
    url(r'^(?P<uuid>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})/$', ProductDetail.as_view(), name='product-detail'),
    url(r'^(?P<uuid>[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})/(?P<code>[^/]+)/$', PurchaseConfirmation.as_view(), name='purchase-confirmation'),
    url(r'^$', ProductList.as_view(), name='product-list'),
    ]
