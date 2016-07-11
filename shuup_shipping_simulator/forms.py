# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries import Countries


class PostalCodeShippingSimulatorForm(forms.Form):
    postal_code = forms.CharField(label=_(u"Postal code"), required=True)


class CityStateCountryShippingSimulatorForm(forms.Form):
    country = forms.ChoiceField(choices=lambda: Countries(), required=True)
    region = forms.CharField(required=True)
    city = forms.CharField(required=True)
