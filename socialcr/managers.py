#!/usr/bin/env python3
import pdb
import git
import yaml
import os
import hashlib
import re
import logging
from logging import *
import pdb

class Manager:
    """ Abstract class for managers """
    
    def __init__(self):
        self._logger = None

class GitManager(Manager):
    """
    Mediator for accessing git functionality in Social CR

    Also contains utility methods 
    """
    
    def __init__(self):
        self._git = None
        self._logger = LogManager(self)

    def git(self):
        """ instantiate git wrapper if not yet created and return it """
        if self._git == None:
            self._git = git.Git()

        return self._git

    def get_repository(self, remote):
        """
        Create a hash from the remote location, create repo, and return it

        If the repository does not exist in the location, it will be created.
        If it does exist, instantiates and returns a git.Repo object
        """

        repo_hash = GitManager.get_hash(remote)
        repo_path = os.path.join(ConfigManager.get_repo_path(), repo_hash)
        self.logger.debug(f"Path to find repository is: {repo_path}")

        if os.path.isdir(repo_path):
            log.debug("Found existing repo")
            return git.Repo(repo_path)
        
        return git.Repo.clone_from(remote, repo_path)

    @classmethod
    def get_username(cls, remote):
        """
        Parses for the username from remote git url and returns it

        >>> GitManager.get_username("https://github.com/tcstang/social-cr.git")
        'tcstang'

        >>> GitManager.get_username("https://bitbucket.org/tortoisehg/hgtk") 
        'tortoisehg'

        >>> GitManager.get_username("git@github.com:tcstang/social-cr.git")
        'tcstang'
        """

        return cls._split_remote(remote)[-2]

    @classmethod
    def get_repo_name(cls, remote):
        """
        Parses for the repository name from remote git url and returns it

        >>> GitManager.get_repo_name("https://github.com/tcstang/social-cr.git")
        'social-cr'

        >>> GitManager.get_repo_name("https://bitbucket.org/tortoisehg/hgtk") 
        'hgtk'

        >>> GitManager.get_repo_name("git@github.com:tcstang/social-cr.git")
        'social-cr'
        """

        return cls._split_remote(remote)[-1].replace(".git", "")

    @classmethod
    def get_host(cls, remote):
        """
        Parses for the host (bitbucket, github) from remote git url and returns it

        >>> GitManager.get_host("https://github.com/tcstang/social-cr.git")
        'github.com'

        >>> GitManager.get_host("https://bitbucket.org/tortoisehg/hgtk") 
        'bitbucket.org'

        >>> GitManager.get_host("git@github.com:tcstang/social-cr.git")
        'github.com'
        """

        return cls._split_remote(remote)[-3].replace("git@", "")


    @classmethod
    def _split_remote(cls, remote):
        """ splits the remote git url up by delimiters and returns list """

        delimiter_regex = re.compile('[/|:]')
        return re.split(delimiter_regex, remote)

    @classmethod
    def get_hash(cls, remote):
        """
        Creates a SHA256 hash from concatenation of host, username, repo and returns it

        >>> GitManager.get_hash("https://github.com/tcstang/social-cr.git")
        'B4FC1249EE249A31331827A1E90584A85681D647AD657E8305428B9413618E63'
        """
        git_host = cls.get_host(remote)
        username = cls.get_username(remote)
        repo_name = cls.get_repo_name(remote)

        repo_uid = f'{git_host}{username}{repo_name}'.encode('utf-8')
        return hashlib.sha256(repo_uid).hexdigest().upper()



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

class LogManager:
    """
    LogManager is the interface between Social CR and the logging library

    It also serves as a facade to the logging library. In future iterations,
    we can add methods to swap out and use different Loggers at runtime.
    """

    def __init__(self, obj):
        self.logger = SimpleLoggerFactory.get_logger(type(obj).__name__)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

class LogFactory:
    """ Abstract factory for creating loggers """

    @classmethod
    def get_logger(cls, name):
        raise NotImplementedError( "Should have implemented this" )

class SimpleLoggerFactory(LogFactory):
    """ A simple, typical, static, logger """

    @classmethod
    def get_logger(cls, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(ConfigManager.get_config()["logging"]["output_file"])
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
