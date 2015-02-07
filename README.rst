Konf
====

Designed to simplify a process of variables usage in configuration files.
Importing variables to Python must be easy!

Installation:

.. code:: bash

    pip install konf


Features:

-  Easy to use
-  JSON and YAML support out of the box
-  Require typing or validation of all input data for human factor prevention
-  Python 2.7, 3+ compatible
-  Unit-tested
-  Custom format of configuration files can be used

For Python data structures validation used excellent lib
`kolypto/py-good <https://github.com/kolypto/py-good>`__

For YAML parsing used great lib of Kirill Simonov
`PyYAML <http://pyyaml.org/wiki/PyYAML>`__


How to use this library
=======================

It's pretty simple. Just look at the code.

.. code:: python

    from konf import Konf

    k_ = Konf('fruits.yml')
    APPLE = k_('APPLE', basestring)
    ORANGE = k_('ORANGE', basestring)
    BASKET_OF_MANDARINS = k_('BASKET', [basestring])
    NAMED_BANANAS = k_('BANANAS', {'yellow': basestring, 'banana2': basestring})

    k2_ = Konf('grades.json')
    DAVID_GRADE = k2_('DAVID', int)
    MARIA_GRADE = k2_('MARIA', int)

You can find more details and advanced examples about natural validation on
`documentation of the "good" validation library <https://pypi.python.org/pypi/good/>`__


List of supporting Exceptions after abnormal situations
=======================================================

:ValidationError: Raises when data from config file doesn't match to the `type_or_validator` arg

:IncompleteConfig: Raises after trying to get variable that not contained in config file

:ReadError: Raises when config file can't be read

:ParseError: Raises if third-party parser can't parse configuration file

:ReassignmentError: Raises if variable is loading from Konf not for the first time

:FileExtensionError: Raises if extension of the config is not .yml or .json, and `parse_callback` arg is not specified


That's it!
==========

Pull-requests are welcome.
