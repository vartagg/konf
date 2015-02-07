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
            'khrum': 'bar',
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
        self.assertRaises(Konf.IncompleteConfig,
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
