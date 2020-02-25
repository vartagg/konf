# -*- coding: utf-8 -*-
from unittest import TestCase
from konf import Konf
import os
import sys

__author__ = 'vartagg'

if sys.version_info >= (3, 0,):
    STRING = str
else:
    STRING = basestring


class KonfigTestCase(TestCase):
    def _get_asset(self, name):
        return os.path.abspath(os.path.join(*[os.path.dirname(__file__), 'assets', name]))

    def test_yaml(self):
        k_ = Konf(self._get_asset('1.yml'))

        a = k_('a', int)
        self.assertEqual(a, 13)

        b = k_('b', STRING)
        self.assertEqual(b, 'foo')

        c = k_('c', float)
        self.assertEqual(c, 4.44)

        cool_list = k_('cool_list', [int])
        self.assertEqual(cool_list, [6, 12])

        coold_dict = k_('cool_dict', {'khrum': STRING, 'dfght': int})
        self.assertEqual(coold_dict, {
            'khrum': u'бар',
            'dfght': 90
        })

    def test_json(self):
        k_ = Konf(self._get_asset('1.json'))

        foo = k_('foo', STRING)
        self.assertEqual(foo, 'TheBar!')

        my_list = k_('my_list', [STRING])
        self.assertEqual(my_list, ['the_first', 'the_next'])

    def test_wrong_extension(self):
        self.assertRaises(Konf.FileExtensionError,
                          lambda: Konf(self._get_asset('1.wrong'))
                          )

    def test_cant_access(self):
        self.assertRaises(Konf.ReadError,
                          lambda: Konf(self._get_asset('99.yml'))
                          )

    def test_cant_load(self):
        self.assertRaises(Konf.ParseError,
                          lambda: Konf(self._get_asset('bad.json'))
                          )

    def test_incomplete_config(self):
        k_ = Konf(self._get_asset('1.yml'))
        self.assertRaises(Konf.IncompleteConfigError,
                          lambda: k_('I_Want_This_Please', int)
                          )

    def test_validation_error(self):
        k_ = Konf(self._get_asset('1.yml'))
        self.assertRaises(Konf.ValidationError,
                          lambda: k_('b', int)
                          )

    def test_multiple_loading(self):
        k_ = Konf(self._get_asset('1.yml'))
        a = k_('a', int)
        self.assertRaises(Konf.ReassignmentError,
                          lambda: k_('a', int)
                          )

    def test_default(self):
        k_ = Konf(self._get_asset('1.yml'))

        x = k_('x', int, 777)
        self.assertEqual(x, 777)

        y = k_('y', dict, 888)
        self.assertEqual(y, 888)

        z = k_('z', float, None)
        self.assertEqual(z, None)

    def test_involved(self):
        k_ = Konf(self._get_asset('2.yml'))
        checker = k_.check_redundant

        right_foot = k_('right_foot', int)
        self.assertEqual(right_foot, 1)
        self.assertRaises(Konf.RedundantConfigError, checker)

        left_foot = k_('left_foot', int)
        checker()
        self.assertEqual(left_foot, 0)

    def test_redundant(self):
        k_ = Konf(self._get_asset('2.yml'))
        checker = k_.check_redundant

        right_foot = k_('right_foot', int)
        self.assertEqual(right_foot, 1)
        self.assertRaises(Konf.RedundantConfigError, checker)

        left_foot = k_('left_foot', int)
        checker()
        self.assertEqual(left_foot, 0)

    def test_involved_with_default(self):
        k_ = Konf(self._get_asset('2.yml'))
        checker = k_.check_redundant
        right_foot = k_('right_foot', int)
        left_foot = k_('left_foot', int)
        tail = k_('tail', int, 9)
        checker()
        self.assertEquals([left_foot, right_foot, tail], [0, 1, 9])

        self.assertRaises(k_.ReassignmentError, lambda: k_('tail', int, 10))

    def test_no_content(self):
        for module in ['3.yml', '4.yml']:
            k_ = Konf(self._get_asset(module))
            self.assertRaises(Konf.IncompleteConfigError, lambda: k_('i_am_not_in_file', int))

    def test_no_content_default(self):
        for module in ['3.yml', '4.yml']:
            k_ = Konf(self._get_asset(module))
            a = k_('i_am_not_in_file_but_with_default', int, 3)
            self.assertEqual(a, 3)

    def test_validators(self):
        # 0. Select configuration file
        k_ = Konf(self._get_asset('5.yml'))

        # 1. Declare validators
        # You can cache validators inside a Konf object as if it's a standard python dict
        k_['v1'] = {
            'key': STRING,
            'secret': STRING,
        }
        k_['v2'] = {
            'key': STRING,
            'secret': STRING,
            'public_name': STRING
        }

        # 2. Get variables from config
        # For avoid copy-paste and massive chunks of code, just declare a new variable
        # and pass data from config to it
        sn_ = k_('SN', {
            'vk': k_['v1'],  # You can get validator you want, for example v1...
            'google': k_['v1'],
            'twitter': k_['v1'],
            'ok': k_['v2']  # ...or v2
        })

        # 3. Fill everything to a python variables which are required for 3rd-party library
        SOCIAL_AUTH_VK_OAUTH2_KEY = sn_['vk']['key']
        SOCIAL_AUTH_VK_OAUTH2_SECRET = sn_['vk']['secret']
        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = sn_['google']['key']
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = sn_['google']['secret']
        SOCIAL_AUTH_TWITTER_KEY = sn_['twitter']['key']
        SOCIAL_AUTH_TWITTER_SECRET = sn_['twitter']['secret']
        SOCIAL_AUTH_ODNOKLASSNIKI_KEY = sn_['ok']['key']
        SOCIAL_AUTH_ODNOKLASSNIKI_SECRET = sn_['ok']['secret']
        SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = sn_['ok']['public_name']

        # 4. Check that config doesn't contain some garbage
        # (this might mean you forgot to get these variables, or this config is wrong, some draft for example)
        k_.check_redundant()

        # 5. If server is running without errors, and you will meet issue with this 3rd-party library later,
        # you can be sure that problem isn't in your configuration file.
        # Otherwise, you'll just catch a error on a start server stage.

        from good import Optional
        k2_ = Konf(self._get_asset('6.yml'))
        k2_['sn_data'] = {
            'key': STRING,
            'secret': STRING,
            Optional('public_name'): STRING
        }
        sn2_ = lambda: k2_('SN', {
            name: k2_['sn_data'] for name in ['vk', 'google', 'twitter']
        })
        self.assertRaises(Konf.ValidationError, sn2_)

        def assign():
            k_['v1'] = {'foo': 'bar'}

        self.assertRaises(Konf.ValidatorManagementError, assign)
        self.assertRaises(Konf.ValidatorManagementError, lambda: k_['v3'])

    def test_nested_default_value(self):
        from good import Any, Default
        k_ = Konf(self._get_asset('1.yml'))
        cool_dict = k_('cool_dict', dict(
            khrum=str,
            dfght=int,
            foo=Any(str, Default('bar'))
        ))
        self.assertEqual(cool_dict['foo'], 'bar')
