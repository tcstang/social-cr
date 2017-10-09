#!/usr/bin/env python

class ConfigManager:
    """
    Mediator for getting and setting config
    """

    @staticmethod
    def get_repo_path():
        """ retrieve the directory that stores repositories """
        return ConfigManager.get_config()["repo_path"]

    @staticmethod
    def get_config():
        """ create the yml parser and return it """
        with open('config/config.yml', 'r') as config_file:
            return yaml.load(config_file)
