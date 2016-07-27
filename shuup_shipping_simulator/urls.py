# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shuup_shipping_simulator.views import ProductShippingSimulatorView, \
    BasketShippingSimulatorView

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^product/simulate_shipping/$',
        ProductShippingSimulatorView.as_view(),
        name='simulate-product-shipping'),

    url(r'^basket/simulate_shipping/$',
        BasketShippingSimulatorView.as_view(),
        name='simulate-basket-shipping'),
)
