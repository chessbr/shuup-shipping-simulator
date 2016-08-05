# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from shuup.utils.importing import cached_load
from shuup.xtheme.plugins._base import TemplatedPlugin
from shuup.xtheme.plugins.forms import TranslatableField

from django.core.urlresolvers import resolve, Resolver404
from django.utils.translation import ugettext_lazy as _


class ShippingSimulatorPlugin(TemplatedPlugin):
    """
    Plugin to simulate shipping methods in product detail page
    """
    identifier = "shipping_simulator.product_shipping_methods"
    name = _("Shipping methods simulator")
    template_name = "plugins/shipping_methods.jinja"
    fields = [
        ("title", TranslatableField(label=_("Title"), required=False, initial="Simulate shipping")),
    ]

    def is_context_valid(self, context):
        is_valid = super(ShippingSimulatorPlugin, self).is_context_valid(context)

        if is_valid:
            try:
                resolved = resolve(context["request"].path)
                is_valid = (resolved.view_name in ("shuup:product", "shuup:basket"))

                # at least one product in basket
                if resolved.view_name == "shuup:basket":
                    is_valid = len(context["request"].basket.product_ids) > 0

            except Resolver404:
                is_valid = False

        return is_valid

    def get_context_data(self, context):
        context_data = super(ShippingSimulatorPlugin, self).get_context_data(context)
        resolved = resolve(context["request"].path)

        # Only works on ProductDetailView
        if resolved.view_name in ("shuup:product", "shuup:basket"):
            context_data["title"] = self.get_translated_value("title")
            context_data["form"] = cached_load("SHIPPING_SIMULATOR_CLASS_SPEC")().get_form()
            context_data["from_session"] = (resolved.view_name == "shuup:basket")

        return context_data
