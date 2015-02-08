Konf
====

Designed to simplify the use of variables in configuration files.
Import variables to Python must be easy and reliable!

Installation:

.. code:: bash

    pip install konf

Running tests:

.. code:: bash

    nosetests


Features:

-  Easy to use
-  JSON and YAML support out of the box
-  Require typing or validation of all input data for human factor prevention
-  Python 2.7, 3+ compatible
-  Unit-tested
-  Custom format of configuration files can be used

For Python data structures validation is used excellent lib
`kolypto/py-good <https://github.com/kolypto/py-good>`__

For YAML parsing is used great lib of Kirill Simonov
`PyYAML <http://pyyaml.org/wiki/PyYAML>`__


Quick start
===========

Just look at the code.

.. code:: python

    from konf import Konf

    # Filling of variables from config file fruits.yml in k_ object
    k_ = Konf('fruits.yml')

    # Getting variables from k_. 1st arg is a name of variable (specified in config),
    # 2nd can be a type or validator
    APPLE = k_('APPLE', basestring)
    ORANGE = k_('ORANGE', basestring)

    # In the next example is using validator: list, that must contain only objects with
    # basestring type (str or unicode)
    BASKET_OF_MANDARINS = k_('BASKET', [basestring])

    # And dict with two required keys with appropriate types
    NAMED_BANANAS = k_('BANANAS', {'yellow': basestring, 'banana2': basestring})

    # Other example with grades.json file
    k2_ = Konf('grades.json')

    DAVID_GRADE = k2_('DAVID', int)
    MARIA_GRADE = k2_('MARIA', int)

You can find more details and advanced examples about natural validation on
`documentation of the "good" validation library <https://pypi.python.org/pypi/good/>`__


Default values
==============

Do you need to use a value if any variable is not contained in a config file? You can use default value.

.. code:: python

    from konf import Konf

    k_ = Konf('extra.yml')

    # 3rd arg is a default. If variable STRICT is not contained in config file,
    # USE_STRICT will be False
    USE_STRICT = k_('STRICT', bool, False)

    # You can also use None as default value
    WINNER = k_('WINNER', int, None)

    # Default values will never be validated, because you forcibly declaring it.
    # So, the next example is legit.
    SHIFT_TIME = k_('SHIFT', int, complex(42, 42))


Checking not involved variables
===============================

Sometimes you want to be sure that all of the variables in a config file are involved and you haven't forgotten anything.
In this situation the ``check_involved()`` method can be helpful.

.. code:: python

    from konf import Konf

    k_ = Konf('required.yml')

    IMPORTANT_1 = k_('IMPORTANT_1', int)

    IMPORTANT_2 = k_('IMPORTANT_2', int)

    # If config file contains anything except IMPORTANT_1 and IMPORTANT_2,
    # RedundantConfigError will be raised after call of this method!
    k_.check_involved()

Default values and ``check_involved()`` also working fine together.

.. code:: python

    from konf import Konf

    k_ = Konf('foo.yml')

    X = k_('X', int, 0)

    Y = k_('Y', int, 0)

    # If X and Y doesn't contained in the config file, RedundantConfigError will not be raised,
    # just X == 0 and Y == 0
    k_.check_involved()


List of supporting Exceptions
=============================

:ValidationError: Raises when data from config file doesn't match to the ``type_or_validator`` arg

:IncompleteConfig: Raises after trying to get variable that not contained in a config file

:ReadError: Raises when config file can't be read

:ParseError: Raises if third-party parser can't parse configuration file

:ReassignmentError: Raises if variable loaded not for the first time

:FileExtensionError: Raises if extension of the config is not .yml or .json, and ``parse_callback`` arg is not specified

:RedundantConfigError: Raises after ``check_involved()`` call if any of variables in config file is not involved in the program
