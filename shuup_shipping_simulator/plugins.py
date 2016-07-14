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
    name = _("Product shipping methods simulator")
    template_name = "plugins/product_shipping_methods.jinja"
    fields = [
        ("title", TranslatableField(label=_("Title"), required=False, initial="Simulate shipping")),
    ]

    def get_context_data(self, context):
        context_data = super(ShippingSimulatorPlugin, self).get_context_data(context)

        try:
            resolved = resolve(context_data["request"].path)

            # Only works on ProductDetailView
            if resolved.view_name == 'shuup:product':
                context_data['title'] = self.get_translated_value("title")
                context_data["form"] = cached_load("SHIPPING_SIMULATOR_CLASS_SPEC")().get_form()

        except Resolver404:
            # we are not in ProductDetailView
            pass

        return context_data
