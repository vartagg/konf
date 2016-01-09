|Build Status|

Konf
====

Tiny tool that designed to solve problems of Python configuration files located outside of VCS.


Installation:

.. code:: bash

    pip install konf

Running tests:

.. code:: bash

    nosetests


Why Konf?
=========

Sometimes there is a need to get some settings outside of Python code and then to use them in an application. This can be secret keys, authentication tokens, URLs of third-party services, or other settings which depends on the server. Developers (or IT engineers) are faced with several challenges:


-  Validation of data importing from config. It may be simple typing, matching with range of possible values or with regexes.
-  Respect of all settings. Check that config contains all required data. Also, it can be useful to check that there are no extra (redundant) things inside a config (because it can be the data, forgotten to consider in an application).
-  Understanding what happens when something goes wrong. Correct representational exceptions allows immediately understand (just having looked at logs) what the problem is. Useful when deploying servers.


Features:
=========

-  Allows to DRY import variables
-  Readability for humans
-  JSON and YAML support out of the box (In fact, additional libraries will be automatically installed for support it)
-  Typing or validation of all importing data. And this is **required** because human factor prevention
-  Python 2.7, 3+ compatible
-  100% code coverage
-  Custom format of configuration files can be used. If I missed and at now anyone uses something else except of supported formats, you can create an `issue <https://github.com/vartagg/konf/issues>`__ about it, and probably the new format will be supported in next versions.

For Python data structures validation is used excellent library
`kolypto/py-good <https://github.com/kolypto/py-good>`__

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
page


Ok, what happened next? Imagine that tokens.yaml is missing. In case of this, after the script execution, we can see next exception message:

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


More complex example
====================

Write the content to a social_auth.yml in a readable form:

.. code:: yaml

   ---
     SN:
       vk:
         key: '123'
         secret: qwerty
       google:
         key: '456'
         secret: uiop
       twitter:
         key: '789'
         secret: zxc
       ok:
         key: '000'
         secret: vbn
         public_name: m

Step-by-step process it in settings.py

.. code:: python

   # 0. Select configuration file
   k_ = Konf('social_auth.yml')

   # 1. Declare validators
   # You can cache validators inside a Konf object as if it's a standard python dict
   k_['v1'] = {
      'key': basestring,
      'secret': basestring,
   }
   k_['v2'] = {
      'key': basestring,
      'secret': basestring,
      'public_name': basestring
   }

   # 2. Get variables from config
   # For avoid copy-paste and massive chunks of code, just declare a new variable
   # and pass data from config to it
   sn = k_('SN', {
      'vk': k_['v1'],  # You can choose validator you want, for example v1...
      'google': k_['v1'],
      'twitter': k_['v1'],
      'ok': k_['v2']  # ...or v2
   })

   # 3. Fill everything to a python variables which are required for 3rd-party library
   SOCIAL_AUTH_VK_OAUTH2_KEY = sn['vk']['key']
   SOCIAL_AUTH_VK_OAUTH2_SECRET = sn['vk']['secret']
   SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = sn['google']['key']
   SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = sn['google']['secret']
   SOCIAL_AUTH_TWITTER_KEY = sn['twitter']['key']
   SOCIAL_AUTH_TWITTER_SECRET = sn['twitter']['secret']
   SOCIAL_AUTH_ODNOKLASSNIKI_KEY = sn['ok']['key']
   SOCIAL_AUTH_ODNOKLASSNIKI_SECRET = sn['ok']['secret']
   SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = sn['ok']['public_name']

   # 4. Check that config doesn't contain some garbage
   # (this might mean you forgot to get these variables, or this config is wrong, some draft for example)
   k_.check_redundant()

   # 5. If server is running without errors, and you will meet issue with this 3rd-party library later,
   # you can be sure that problem isn't in your configuration file.
   # Otherwise, you'll just catch a error on a start server stage.

List of supported Exceptions
============================


========================     ===================================================================================
     Exception                                     Raises when...
========================     ===================================================================================
ValidationError              Data from config file doesn't match to the ``type_or_validator`` arg

IncompleteConfigError        Trying to get variable that not contained in a config file

ReadError                    Config file can't be read

ParseError                   Third-party parser can't parse configuration file

ReassignmentError            Variable is loaded not for the first time

FileExtensionError           Extension of the config isn't supported, and ``parse_callback`` arg isn't specified

RedundantConfigError         Call of ``check_redundant()`` if any of variables in a config isn't used in app

ValidatorManagementError     Incorrect usage of validators
========================     ===================================================================================

.. |Build Status| image:: https://travis-ci.org/vartagg/konf.svg?branch=master
   :target: https://travis-ci.org/vartagg/konf
