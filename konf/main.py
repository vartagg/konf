# -*- coding: utf-8 -*-
import yaml
import json
import os

__author__ = 'vartagg'

try:
    from good import Schema, Invalid
except ImportError:
    from voluptuous import Schema, Invalid


MAPPING = {
    '.yml': yaml.safe_load,
    '.yaml': yaml.safe_load,
    '.json': json.loads
}


class Unspecified(object):
    pass


class Konf(object):
    class FileExtensionError(Exception):
        pass

    class IncompleteConfigError(Exception):
        pass

    class ReadError(Exception):
        pass

    class ParseError(Exception):
        pass

    class ValidationError(Exception):
        pass

    class ReassignmentError(Exception):
        pass

    class RedundantConfigError(Exception):
        pass

    def __init__(self, config_path, parse_callback=None, *parse_callback_args, **parse_callback_kwargs):
        """
        File extension detection, reading content from file, parsing and encapsulation data inside Konf object.

        :param config_path: path to the config file
        :param parse_callback: if specified, this function will be used  for parsing config
        :param parse_callback_args: the *args passing to the parse_callback if it's specified
        :param parse_callback_kwargs: the **kwargs passing to the parse_callback if it's specified
        :return: new Konf object
        """
        self._config = config_path
        self._data = list()
        if parse_callback is not None:
            self._load = parse_callback
        else:
            extension = self._detect_extension(config_path)
            try:
                self._load = MAPPING[extension]
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

    def __call__(self, name, type_or_validator, default=Unspecified):
        """
        Getting a variable from config file is here.

        :param name: variable name in the config file
        :param type_or_validator: how validate this variable
        :param default: if specified, after failed getting a variable from config, this default will be used
        :return: variable from config file
        """
        if self._is_collected(name):
            raise self.ReassignmentError('Variable {} is already loaded'.format(name))

        if not isinstance(type_or_validator, Schema):
            type_or_validator = Schema(type_or_validator)

        default_is_specified = default is not Unspecified
        default_is_used = False

        try:
            value = self._load_from_file_entry(name)
        except self.IncompleteConfigError:
            if default_is_specified:
                value = default
                default_is_used = True
                self._data[name] = value
            else:
                raise

        if not default_is_used:
            # Validate only if it is not default value
            try:
                type_or_validator(value)
            except Invalid as e:
                raise self.ValidationError(e)
        self._collected_data.append(name)

        return value

    def check_involved(self):
        data_set = set(self.data)
        collected_data_set = set(self.collected_data)
        diff = data_set - collected_data_set
        if diff:
            raise self.RedundantConfigError('There are unused variables in the config file "{}":'
                                            '\n{}'.format(self._config, ', '.join(map(lambda x: str(x), diff))))

    @property
    def path(self):
        return self._config

    @property
    def data(self):
        return self._data

    @property
    def collected_data(self):
        return self._collected_data

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
            raise self.IncompleteConfigError('Param {} not found in the configuration file "{}"'.
                                        format(name, self.path))
        return ret
