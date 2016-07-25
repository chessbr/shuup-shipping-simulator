# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import unicode_literals

import decimal
import logging

from shuup.core.models._products import Product
from shuup.utils.i18n import format_money
from shuup.utils.importing import cached_load
from shuup.utils.numbers import parse_decimal_string

from django.http.response import HttpResponseBadRequest, JsonResponse
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.views.generic.base import View

logger = logging.getLogger(__name__)


class ShippingSimulatorView(View):

    def post(self, request, **kwargs):
        """
        Calculates and returns a JSON object containing a
        list of available methods in the format:
            [
                {
                    "name": "Method name #1",
                    "price": 3.41,
                    "formatted_price": "U$ 3.41",
                    "time_days":{
                        "min": 1,
                        "max": 3
                    }
                },
                {
                    "name": "Method name #2",
                    "price": 19.2,
                    "formatted_price": "U$ 19.20",
                },
                {
                    "name": "Method name #3",
                    "price": 0.0,
                    "formatted_price": "U$ 0.00",
                    "time_days":{
                        "min": 5
                    }
                },
                ...
            ]

        A temporary basket is created and the product with quantity
        is added to it. Then the shipping methods can be calculated normally
        """

        shipping_simulator = cached_load("SHIPPING_SIMULATOR_CLASS_SPEC")()
        shipping_form = shipping_simulator.get_form(data=request.POST)

        if shipping_form.is_valid():
            # create temp basket
            tmp_basket = cached_load("SHUUP_BASKET_CLASS_SPEC")(request)

            # sets the shipping addres used to calculate the price and the delivery time
            tmp_basket.shipping_address = shipping_simulator.get_shipping_address(shipping_form)

            # from shuup/front/basket/commands.py:handle_add()
            # fetches the product object
            product_id = int(request.POST['product_id'])
            product = Product.objects.get(pk=product_id)
            shop_product = product.get_shop_instance(shop=request.shop)
            if not shop_product:
                logger.error(_("Product ID {0} not available in {1} shop").format(product_id, request.shop))
                return HttpResponseBadRequest()

            if request.POST.get('supplier_id'):
                supplier = shop_product.suppliers.filter(pk=request.POST['supplier_id']).first()
            else:
                supplier = shop_product.suppliers.first()

            # validate and format the quantity
            try:
                quantity = parse_decimal_string(request.POST['quantity'])
                if not product.sales_unit.allow_fractions:
                    if quantity % 1 != 0:
                        logger.error(_("The quantity %f is not allowed. Please use an integer value.") % quantity)
                        return HttpResponseBadRequest()

                    quantity = int(quantity)
            except (ValueError, decimal.InvalidOperation) as e:
                logger.exception(_("The quantity is not valid: {0}").format(e))
                return HttpResponseBadRequest()

            if quantity <= 0:
                logger.error(_("The quantity %s is not valid.") % quantity)
                return HttpResponseBadRequest()

            # create the dict to use in add_product
            add_product_kwargs = {
                "product": product,
                "quantity": quantity,
                "supplier": supplier,
                "shop": request.shop,
            }

            tmp_basket.add_product(**add_product_kwargs)
            methods = []

            # iterate over all available methods and calculates the price and delivery time
            for m in tmp_basket.get_available_shipping_methods():
                cost = m.get_total_cost(tmp_basket)
                time = m.get_shipping_time(tmp_basket)

                method = {
                    'name': m.get_effective_name(tmp_basket),
                    'formatted_cost': format_money(cost.price, digits=2),
                    'cost': float(cost.price.value),
                }

                # some methods just return None, others doesnt have a max_duration
                if time:
                    if time.max_duration and time.max_duration > time.min_duration:
                        method['time'] = {
                            "min": time.min_duration.days,
                            "max": time.max_duration.days,
                            "formatted": _("{0}-{1} days").format(time.min_duration.days,
                                                                  time.max_duration.days)
                        }
                    else:
                        method['time'] = {
                            "min": time.min_duration.days,
                            "formatted": ungettext("{0} day", "{0} days",
                                                   time.min_duration.days).format(time.min_duration.days)
                        }

                methods.append(method)

            return JsonResponse({"methods": methods})

        return JsonResponse({})
