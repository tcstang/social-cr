#!/usr/bin/env python3
import pdb
import git
import yaml
import os
import hashlib
import re
from helpers.decorators import Singleton

class GitManager:
    """
    Mediator for accessing git functionality in Social CR

    Also contains utility methods 
    """
    
    def __init__(self):
        """ lazy instance of git """
        self.__git = None

    def git(self):
        """ instantiate git wrapper if not yet created and return it """
        if self.__git == None:
            self.__git = git.Git()

        return self.__git

    def get_repository(self, remote):
        """
        Create a hash from the remote location, create repo, and return it

        If the repository does not exist in the location, it will be created.
        If it does exist, instantiates and returns a git.Repo object
        """
        repo_hash = GitManager.get_hash(remote)
        repo_path = os.path.join(ConfigManager.get_repo_path(), repo_hash)

        if os.path.isdir(repo_path):
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

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
