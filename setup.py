# -*- coding: utf-8 -*-
# This file is part of Shuup Shipping Simulator.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import setuptools

NAME = 'shuup-shipping-simulator'
VERSION = '1.0.0'
DESCRIPTION = 'Product shipping methods simulator plugin for Shuup'
AUTHOR = 'Rockho Team'
AUTHOR_EMAIL = 'rockho@rockho.com.br'
URL = 'http://www.rockho.com.br/'
LICENSE = 'AGPL-3.0'

EXCLUDED_PACKAGES = [
    'shuup_shipping_simulator_tests', 'shuup_shipping_simulator_tests.*',
]

REQUIRES = [
]

if __name__ == '__main__':
    setuptools.setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        url=URL,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        packages=["shuup_shipping_simulator"],
        include_package_data=True,
        install_requires=REQUIRES,
        entry_points={"shuup.addon": "shuup_shipping_simulator=shuup_shipping_simulator"}
    )
