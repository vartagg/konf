Konf
====

Killer-library that once and for all solve the problem of Python configuration files outside of VCS.


Installation:

.. code:: bash

    pip install konf

Running tests:

.. code:: bash

    nosetests


Why Konf?
=========

Sometimes there is a need to get some settings out from the Python code, and then to use them in an application. It can be secret keys, authentication tokens, URLs of third-party services, or other params which may be different on other servers. A developer (or IT engineer) is faced with several challenges:


-  Validation of data importing from config. He may need for simple typing, range of values or matching with regexes.
-  Data integrity. He must be sure that all the complex data structures (lists or dicts for example) represents the required schemas. Also, it can be useful to check whether there are no extra (redundant) things inside a config (because it can be a data forgotten to map inside an application).
-  Correct exceptions when something goes wrong. This allows immediately understand (just having looked at logs) of what the problem is. Useful when deploying servers.


Features:
=========

-  Readability and user-friendly for humans (Yes, IT specialists are also, in part, humans)
-  JSON and YAML support out of the box (In fact, additional libraries will be automatically installed for support it ^_^ )
-  Typing of validation of all importing data. And this will be **required** for human factor prevention
-  Python 2.7, 3+ compatible
-  100% code coverage
-  Custom format of configuration files can be used. If I missed and at now anyone uses something else except of JSON and YAML, you can create an `issue <https://github.com/vartagg/konf/issues>`__ about it, and probably the new format will be supported in next versions.

For Python data structures validation is used one of these excellent libs:

-  `kolypto/py-good <https://github.com/kolypto/py-good>`__ (by default, because more functionality)
-  `alecthomas/voluptuous <https://github.com/alecthomas/voluptuous>`__ (fundamental library on which *good* based, optional)

For YAML parsing is used a great lib of Kirill Simonov
`PyYAML <http://pyyaml.org/wiki/PyYAML>`__


Quick start
===========

Just look at the code.

.. code:: python

    from konf import Konf

    # Filling of variables from config file tokens.yaml in k_ object
    k_ = Konf('tokens.yaml')

    # Getting variables from k_: first argument is a name of variable (specified in the config),
    # second can be a type or validator
    SECRET_KEY = k_('secret_key', basestring)
    AUTH_TOKEN = k_('auth_token', basestring)

    # In the next example is used a validator: list, that must contain
    # only objects with basestring type (str or unicode)
    CLIENTS = k_('clients', [basestring])

    # And dict with two required keys with appropriate types
    DELAYS = k_('delays', {'case1': int, 'case2': int})



You can find more details and advanced examples about natural validation on
`good <https://pypi.python.org/pypi/good>`__
or
`voluptuous <https://pypi.python.org/pypi/voluptuous>`__
pages.


Ok, what happened next? Let us assume tokens.yaml is missing. In case of this, after the script execution, we can see next exception message:

.. code:: pytb

    konf.main.ReadError: Can`t access to the configuration file "tokens.yaml"


Let's create a file tokens.yaml and input next:

.. code:: yaml

    ---
      secret_key: FOO
      auth_token: BAR
      clients: Q,
      delays:
        case1: 15
        case2: 17


Exception is raised:

.. code:: pytb

    Traceback (most recent call last):
      File "/Users/me/python/examples/example.py", line 19, in <module>
        CLIENTS = k_('clients', [basestring])
      File "/Users/me/python/examples/konf/konf/main.py", line 126, in __call__
        raise self.ValidationError(e)
    konf.main.ValidationError: expected a list


Then fix this mistake:

.. code:: yaml

    ---
      secret_key: FOO
      auth_token: BAR
      clients: [Q]
      delays:
        case1: 15
        case2: 17


Now all be OK, because ``[Q]`` represents a list of values, not a string. **Note**: you can see the list of all supported exceptions in the end of this documentation page. 


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


Checking redundant variables
============================

Sometimes you want to be sure that all of the variables in a config file are used and you haven't forgotten anything.
In this situation the ``check_redundant()`` method can be helpful.

.. code:: python

    from konf import Konf

    k_ = Konf('bar.yaml')

    FOO1 = k_('foo1', int)

    FOO2 = k_('foo2', int)

    # If config file contains anything except foo1 and foo2,
    # RedundantConfigError will be raised after call of this method!
    k_.check_redundant()  # Fail


Default values and ``check_redundant()`` also working fine together.

.. code:: python

    from konf import Konf

    k_ = Konf('foo.yaml')

    X = k_('X', int, 0)

    Y = k_('Y', int, 0)

    # If X and Y doesn't contained in the config file, RedundantConfigError will not be raised
    # after next line of code, because they have default values. 
    # So, it's just like X == 0 and Y == 0
    k_.check_redundant()  # Success


List of supported Exceptions
============================


=====================  ====================================================================================
     Exception                                     Raises when...
=====================  ====================================================================================
ValidationError        Data from config file doesn't match to the ``type_or_validator`` arg

IncompleteConfigError  Trying to get variable that not contained in a config file

ReadError              Config file can't be read

ParseError             Third-party parser can't parse configuration file

ReassignmentError      Variable is loaded not for the first time

FileExtensionError     Extension of the config isn't supported, and ``parse_callback`` arg isn't specified

RedundantConfigError   Call of ``check_redundant()`` if any of variables in a config isn't used in app
=====================  ====================================================================================
