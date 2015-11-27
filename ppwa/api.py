import os
import logging

import requests
from django.conf import settings

logger = logging.getLogger('wwpa.api')


def product_detail(pid):
    '''Return detail on one product from API.

    :param pid: product id
    :return: {pid, uuid, name, slug, price, cost, inventory_on_hand, description}
    '''
    base = settings.PRODUCT_API_URL.strip('/')
    auth = settings.PRODUCT_API_AUTH
    url = '%s/%s/' % (base, pid, )
    logger.info(url)
    response = requests.get(url, headers={'X-AUTH': auth})
    response.raise_for_status()
    data = response.json()
    return data
