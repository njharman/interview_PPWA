import logging

import requests
from django.conf import settings

logger = logging.getLogger('ppwa.api')

# Users of api should't import requests to catch exceptions.
HTTPError = requests.HTTPError


def product_list():
    '''Product listing.
    :return: list of {id, uuid, slug, name}
    :raise ValueError: JSON parsing issues.
    :raise HTTPError: various networking issues.
    '''
    url = settings.PRODUCT_API_URL
    auth = settings.PRODUCT_API_AUTH
    response = requests.get(url, headers={'X-AUTH': auth})
    logger.info('GET %s: %s' % (response.status_code, url, ))
    response.raise_for_status()
    data = response.json()
    return data


def product_detail(pid):
    '''Return detail on one product from API.

    :param pid: product id.
    :return: {pid, uuid, name, slug, price, cost, inventory_on_hand, description}
    :raise ValueError: JSON parsing issues.
    :raise HTTPError: various networking issues.
    '''
    base = settings.PRODUCT_API_URL.strip('/')
    auth = settings.PRODUCT_API_AUTH
    url = '%s/%s/' % (base, pid, )
    response = requests.get(url, headers={'X-AUTH': auth})
    logger.info('GET %s: %s' % (response.status_code, url, ))
    response.raise_for_status()
    data = response.json()
    return data


def post_purchase(pid, quantity, cust_name, email, phone):
    '''POST purchase order to API.

    :param pid: product id to be purchased.
    :param quantity: quantity to be purchased.
    :param cust_name: Customer name.
    :param email: Customer email.
    :param phone: Customer phone.
    :return: {confirmation_code, }
    :raise ValueError: JSON parsing issues.
    :raise HTTPError: various networking issues.
    '''
    base = settings.PRODUCT_API_URL.strip('/')
    auth = settings.PRODUCT_API_AUTH
    url = '%s/%s/purchase/' % (base, pid, )
    payload = {
            'customer_name': cust_name,
            'customer_email': email,
            'customer_phone': phone,
            'quantity': quantity,
            }
    response = requests.post(url, headers={'X-AUTH': auth}, json=payload)
    logger.info('POST %s: %s' % (response.status_code, url, ))
    response.raise_for_status()
    data = response.json()
    return data
