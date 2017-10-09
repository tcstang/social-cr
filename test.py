#!/usr/bin/env python
from managers.git import *
manager = GitManager()
manager.get_repository("git@github.com:tcstang/test-repository.git")
