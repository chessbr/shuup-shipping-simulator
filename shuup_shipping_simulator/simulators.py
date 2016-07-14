# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from shuup_shipping_simulator.forms import (
    CityStateCountryShippingSimulatorForm, PostalCodeShippingSimulatorForm
)

from shuup.core.models import MutableAddress


class ShippingSimulatorBase(object):
    """
    Shipping base class. Subclass this and override with
    custom implementation
    """

    form_class = None

    def get_form(self, **kwargs):
        """ Returns the form which users will put his address """
        return self.form_class(**kwargs)

    def get_shipping_address(self, form):
        """
        :type: form django.forms.Form
        :param: form Validated Django form

        :rtype: shuup.core.models.MutableAddress
        :return: A configured mutable address that will set in
        Basket `shipping_address` attribute
        """
        return None


class PostalCodeShippingSimulator(ShippingSimulatorBase):
    form_class = PostalCodeShippingSimulatorForm

    def get_shipping_address(self, form):
        """
        Just return a MutableAddress with a postal code set
        """
        return MutableAddress(postal_code=form.cleaned_data['postal_code'])


class CityStateCountryShippingSimulator(ShippingSimulatorBase):
    form_class = CityStateCountryShippingSimulatorForm

    def get_shipping_address(self, form):
        """
        Just return a MutableAddress with city, region and country set
        """
        return MutableAddress(city=form.cleaned_data['city'],
                              region=form.cleaned_data['region'],
                              country=form.cleaned_data['country'])
