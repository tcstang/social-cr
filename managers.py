#!/usr/bin/env python3
import pdb
import git

# this should be a bridge to git library
# that returns useful objects
class GitManager:
    _instance = None

    def git(self):
        if self._instance == None:
            self._instance = git.Git()

        return self._instance

    def clone(self, remote):
        try:
            self.git().clone(remote)
        except:
            print("Clone was unsuccessful")
            return

    def Status(self):
        return Status(self.git())

    def Diff(self):
        return Diff(self.git())

class GitOperation:
    __raw_data = None

    def __init__(self):
        pass

    def get_raw_result():
        return self.__raw_data


class Diff(GitOperation):
    def __init__(self, git):
        self.__raw_data = git.diff()
        
        
class Status(GitOperation):
    branch = None
    merge_required = False
    untracked_files = []
    to_be_committed_files = []

    def __init__(self, git):
        self.__raw_data = git.status()
        lines = self.__raw_data.splitlines()
        self.branch = self.__get_branch(lines)

        
    def __get_branch(self, lines):
        branch = None
        pdb.set_trace()
        for line in lines:
            if "On branch" in line:
                return line.split("On branch", 1)[1].strip()

        if branch == None:
            print("Not found!")
