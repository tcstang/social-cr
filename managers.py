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

    """
    
    def __init__(self):
        self.__git = None

    def git(self):
        if self.__git == None:
            self.__git = git.Git()

        return self.__git

    def get_repository(self, remote):
        repo_hash = GitManager._get_hash(remote)
        repo_path = os.path.join(ConfigManager.get_repo_path(), repo_hash)

        if os.path.isdir(repo_path):
            return git.Repo(repo_path)
        
        return git.Repo.clone_from(remote, repo_path)

    @classmethod
    def get_username(cls, remote):
        """
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
        delimiter_regex = re.compile('[/|:]')
        return re.split(delimiter_regex, remote)

    @classmethod
    def _get_hash(cls, remote):
        """
        >>> GitManager._get_hash("https://github.com/tcstang/social-cr.git")
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
        return ConfigManager.get_config()["repo_path"]

    @staticmethod
    def get_config():
        with open('config/config.yml', 'r') as config_file:
            return yaml.load(config_file)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
