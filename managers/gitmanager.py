#!/usr/bin/env python3
import git

class GitManager:
    _git = None

    def git(self):
        if self._git == None:
            self._git = git.Git()

        return self._git

    def clone_repository(self, remote):
        try:
            self.git().clone(remote)
        except:
            print("nope!")
            return
