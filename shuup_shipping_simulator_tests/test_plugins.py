# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import pytest

from shuup_shipping_simulator.forms import (
    CityStateCountryShippingSimulatorForm, PostalCodeShippingSimulatorForm
)
from shuup_shipping_simulator.plugins import ShippingSimulatorPlugin

from shuup.testing.factories import get_default_product, get_default_shop
from shuup.testing.utils import apply_request_middleware
from shuup.utils.importing import clear_load_cache

from django.core.urlresolvers import reverse
from django.test.utils import override_settings


def get_context(rf, path):
    request = rf.get(path)
    request.shop = get_default_shop()
    apply_request_middleware(request)
    return {"request": request}


@pytest.mark.django_db
@pytest.mark.parametrize("class_spec", ["shuup_shipping_simulator.simulators:PostalCodeShippingSimulator",
                                        "shuup_shipping_simulator.simulators:CityStateCountryShippingSimulator"])
def test_checkout_generator_plugin(rf, class_spec):
    with override_settings(SHIPPING_SIMULATOR_CLASS_SPEC=class_spec):
        product = get_default_product()
        context = get_context(rf, reverse("shuup:product", kwargs={"pk":product.pk, "slug":product.slug}))
        clear_load_cache()

        plugin = ShippingSimulatorPlugin({})

        if class_spec.endswith("PostalCodeShippingSimulator"):
            assert isinstance(plugin.get_context_data(context)["form"], PostalCodeShippingSimulatorForm)

        elif class_spec.endswith("CityStateCountryShippingSimulator"):
            assert isinstance(plugin.get_context_data(context)["form"], CityStateCountryShippingSimulatorForm)

        # wrong path
        context = get_context(rf, "/")
        assert plugin.get_context_data(context).get("form") is None
