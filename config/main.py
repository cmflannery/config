"""config: an open source library for quickly creating and using configuration files"""
from __future__ import print_function, division, absolute_import
import os
from io import open
import pandas as pd


class Configurator(object):
    def __init__(self, standard_types, is_optional=None):
        """
        Parameters
        ----------
        standard_types : dict
            a dictionary containing the expected variable names and their standard types
        is_optional : list, str
            list or single string of keywords in `standard_types` that should be treated as optional
            parameters.
            
            By default, all keywords in `standard_types` are required
        """
        self.standard_types = standard_types
        self.is_optional = is_optional

    def read(self, fname):
        """Parse configuration file and return a dictionary with the key value pairs

        Parameters:
            fname (str): file name, or path to file, of configuration file

        Returns:
            dict: contains all parameters and values parsed and typecast
        """
        assert os.path.isfile(fname), 'Error: {} does not exist in the working directory'.format(fname)
        with open(fname, 'r') as f:
            config = f.readlines()

        config = [c for c in config if c[0] != '#']  # ignore all comment lines
        configuration = {}
        # Read the configuration file and store all key-value pairs in a dictionary
        for thing in config:
            param_value = thing.split(' ')
            try:
                parameter = param_value[0].strip()
                value = param_value[1].strip()
                configuration[parameter] = value
            except IndexError:
                pass

        # Parse through the data and convert types
        for key in configuration.keys():
            try:
                std_type = self.standard_types[key]
            except KeyError:
                raise Exception('Error: {} is not a known configuration parameter'.format(key))

            if std_type != type(configuration[key]):
                configuration[key] = std_type(configuration[key])

        self.config = configuration
        return self.config
