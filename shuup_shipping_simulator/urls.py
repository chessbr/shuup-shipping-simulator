# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shuup_shipping_simulator.views import ShippingSimulatorView

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^product/simulate_shipping/$', ShippingSimulatorView.as_view(), name='simulate-product-shipping'),
)
