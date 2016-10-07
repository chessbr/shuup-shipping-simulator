[![Build Status](https://travis-ci.org/rockho-team/shuup-shipping-simulator.svg?branch=master)](https://travis-ci.org/rockho-team/shuup-shipping-simulator)
[![Coverage Status](https://coveralls.io/repos/github/rockho-team/shuup-shipping-simulator/badge.svg?branch=master)](https://coveralls.io/github/rockho-team/shuup-shipping-simulator?branch=master)
[![License](https://img.shields.io/badge/license-AGPLv3-blue.svg)](LICENSE)

# Shuup Shipping Simulator
A plugin for Shuup to simulate shipping methods in product detail page. Some customers want to see how much a product will cost with shipping and also how long it would take to arrive at home.

The plugin checks the URL to render its content, it means it will only work inside the `ProductDetailView` page.

## How it works

The plugin will render a form to collect the customer address information, that will be used to create an instance of `MutableAddress`. The plugin will send a POST request to the `ShippingSimulatorView` which is responsible for receiving the Shipping Simulator form and the product info.

Inside the `ShippingSimulatorView` a temporary Basket is created with the `MutableAdrress`, the product and the quantity set. The Basket has already methods to return available shipping methods from a source (in this case we use our temp basket). The view then iterate over all available shipping methods and call its `get_total_cost()` and `get_shipping_time()` methods. The results are formatted and put inside a list which is returned by the `ShippingSimulatorView` as a JsonResponse.

The plugin receives the JSON response and present to the customer, simply as that.

## Compatibility
* Shuup v0.5.0
* [Tested on Python 2.7, 3.4 and 3.5](https://travis-ci.org/rockho-team/shuup-shipping-simulator)

## Usage

First, configure the settings of your Django project and set Shipping simulator class through `SHIPPING_SIMULATOR_CLASS_SPEC` config. The default value is `shuup_shipping_simulator.simulators:PostalCodeShippingSimulator`.

Second, edit product detail page usig Xtheme and add Shipping simulator plugin where you want and it's done.

## Customizing
You can create your own shipping simulator. Simply subclass `ShippingSimulatorBase` and override the necessary methods and custom form.

## Contributing
Feel free to contribute. Fork and send a PR! :)

## Tests
To run tests, just run `py.test shuup-shipping-simulator_tests` inside your virtualenv (with this module and Shuup installed).


Copyright
---------

Copyright (C) 2016 by [Rockho Team](https://github.com/rockho-team)


License
-------

Shuup Shipping Simulator is published under the GNU Affero General Public License,
version 3 (AGPLv3) (see the [LICENSE](LICENSE) file).
