# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from datetime import timedelta
import json

from mock import patch
import pytest

from shuup.core.models._service_base import ServiceCost
from shuup.core.models._service_shipping import CustomCarrier
from shuup.testing.factories import (
    get_default_product, get_default_shop, get_default_supplier, get_default_tax_class
)
from shuup.testing.models._behavior_components import ExpensiveSwedenBehaviorComponent
from shuup.utils.dates import DurationRange
from shuup.utils.i18n import format_money
from shuup.utils.importing import clear_load_cache

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.utils import override_settings


@pytest.mark.django_db
@pytest.mark.parametrize("class_spec", ["shuup_shipping_simulator.simulators:PostalCodeShippingSimulator",
                                        "shuup_shipping_simulator.simulators:CityStateCountryShippingSimulator"])
def test_postalcodeshipping(class_spec):

    with override_settings(SHIPPING_SIMULATOR_CLASS_SPEC=class_spec):
        get_default_shop()
        product = get_default_product()

        clear_load_cache()

        carrier = CustomCarrier.objects.create(name="Kustom Karrier")
        service = carrier.create_service(None, enabled=True,
                               shop=get_default_shop(),
                               tax_class=get_default_tax_class(),
                               name="A Kustom Cervise",
                               description="Nice!")

        path = reverse("shuup:simulate-product-shipping")
        client = Client()

        data = {
            "product_id": product.id,
            "command": "add",
            "quantity": "1",
        }

        if class_spec.endswith("PostalCodeShippingSimulator"):
            data["postal_code"] = "37128482"

        elif class_spec.endswith("CityStateCountryShippingSimulator"):
            data["city"] = "Plumenau"
            data["region"] = "SC"
            data["country"] = "BR"

        # First, the method does not return any price. it must be free
        cost = get_default_shop().create_price(0.00)
        response = client.post(path, data)
        json_response = json.loads(response.content.decode("utf-8"))
        method = json_response["methods"][0]
        assert method["name"] == service.name
        assert method["description"] == service.description
        assert method["cost"] == cost.value
        assert method["formatted_cost"] == format_money(cost)
        assert method.get("time") is None

        # now lets add some extra price and time behavior
        service.behavior_components.add(ExpensiveSwedenBehaviorComponent.objects.create())

        cost = get_default_shop().create_price(1.00)
        duration = DurationRange(timedelta(days=5))

        with patch.object(ExpensiveSwedenBehaviorComponent, 'get_costs', return_value=[ServiceCost(cost)]):
            with patch.object(ExpensiveSwedenBehaviorComponent, 'get_delivery_time', return_value=duration):
                response = client.post(path, data)
                json_response = json.loads(response.content.decode("utf-8"))
                method = json_response["methods"][0]

                assert method["name"] == service.name
                assert method["description"] == service.description
                assert method["cost"] == cost.value
                assert method["formatted_cost"] == format_money(cost)
                assert method["time"]["min"] == duration.min_duration.days
                assert not method["time"]["formatted"] is None
                assert method["time"].get("max") is None

        # now with duration range time
        cost = get_default_shop().create_price(3.0)
        duration = DurationRange(timedelta(days=2), timedelta(days=8))

        with patch.object(ExpensiveSwedenBehaviorComponent, 'get_delivery_time', return_value=duration):
            with patch.object(ExpensiveSwedenBehaviorComponent, 'get_costs', return_value=[ServiceCost(cost)]):
                response = client.post(path, data)
                json_response = json.loads(response.content.decode("utf-8"))
                method = json_response["methods"][0]

                assert method["name"] == service.name
                assert method["description"] == service.description
                assert method["cost"] == cost.value
                assert method["formatted_cost"] == format_money(cost)

                assert method["time"]["min"] == duration.min_duration.days
                assert method["time"]["max"] == duration.max_duration.days


        # with suppier id
        data["supplier_id"] = get_default_supplier().pk
        response = client.post(path, data)
        json_response = json.loads(response.content.decode("utf-8"))
        method = json_response["methods"][0]
        assert method["name"] == service.name

        # with fractional quantity - internal error
        data["quantity"] = "1.321"
        response = client.post(path, data)
        assert response.status_code == 400

        # invalid quantity - internal error
        data["quantity"] = "1.,32.,1"
        response = client.post(path, data)
        assert response.status_code == 400

        # negative quantity - internal error
        data["quantity"] = "-1"
        response = client.post(path, data)
        assert response.status_code == 400

        # invalid form
        data = {"produt_id": product.id}
        response = client.post(path, data)
        assert json.loads(response.content.decode("utf-8")) == {}
