# -*- coding: utf-8 -*-
from good import Schema, Invalid
import yaml
import json
import os

__author__ = 'vartagg'


_MAPPING = {
    '.yml': yaml.safe_load,
    '.json': json.loads
}


class Konf(object):
    class FileExtensionError(Exception):
        pass

    class IncompleteConfig(Exception):
        pass

    class ReadError(Exception):
        pass

    class ParseError(Exception):
        pass

    class ValidationError(Exception):
        pass

    class ReassignmentError(Exception):
        pass

    def __init__(self, config_path, parse_callback=None, *parse_callback_args, **parse_callback_kwargs):
        """
        :param config_path: path to the config file
        :param parse_callback: if defined, this function will be used  for parsing config
        :param parse_callback_args: the *args passing to the parse_callback if it's defined
        :param parse_callback_kwargs: the **kwargs passing to the parse_callback if it's defined
        :return: new Konf object
        """
        self._config = config_path
        self._data = list()
        if parse_callback is not None:
            self._load = parse_callback
        else:
            extension = self._detect_extension(config_path)
            try:
                self._load = _MAPPING[extension]
            except KeyError:
                raise self.FileExtensionError('Can`t load data from this file because it`s extension is wrong. '
                                              '\nYou can provide parse_callback if you want to get data from files '
                                              '\nwith non-standard extensions.')
        self._load_callback_args = parse_callback_args
        self._load_callback_kwargs = parse_callback_kwargs

        try:
            with open(self.path, 'r') as f:
                file_entry = f.read()
        except Exception as e:
            raise self.ReadError('Can`t access to the configuration file "{}"'
                                 '\nDetails:\n{}'.format(self.path, e))
        try:
            data = self._load(file_entry, *self._load_callback_args, **self._load_callback_kwargs)
        except Exception as e:
            raise self.ParseError('Can`t load data from the configuration file "{}"'
                                  '\nDetails:\n{}'.format(self.path, e))
        self._data = data
        self._collected_data = []

    def __call__(self, name, type_or_validator):
        """
        :param name: variable name in the config file
        :param type_or_validator: how validate this variable
        :return: variable from config file
        """
        if self._is_collected(name):
            raise self.ReassignmentError('Variable {} is already loaded'.format(name))

        if not isinstance(type_or_validator, Schema):
            type_or_validator = Schema(type_or_validator)
        value = self._load_from_file_entry(name)
        try:
            type_or_validator(value)
        except Invalid as e:
            raise self.ValidationError(e)
        self._collected_data.append(name)
        return value

    @property
    def path(self):
        return self._config

    @property
    def data(self):
        return self._data

    @staticmethod
    def _detect_extension(path):
        return os.path.splitext(path)[-1]

    def _is_collected(self, name):
        return name in self._collected_data

    def _load_from_file_entry(self, name):
        assert name, 'Name of a variable must have not null length'
        try:
            ret = self.data[name]
        except KeyError:
            raise self.IncompleteConfig('Param {} not found in the configuration file "{}"'.
                                        format(name, self.path))
        return ret
