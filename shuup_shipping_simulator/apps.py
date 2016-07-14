# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shuup.apps import AppConfig


class ShuupShippingSimulatorAppConfig(AppConfig):
    name = "shuup_shipping_simulator"
    verbose_name = "Shuup Shipping Simulator"
    provides = {
        "xtheme_plugin": [
            "shuup_shipping_simulator.plugins:ShippingSimulatorPlugin",
        ],
        "front_urls": [
            "shuup_shipping_simulator.urls:urlpatterns"
        ]
    }
