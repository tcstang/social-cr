#!/usr/bin/env python

import os
import re

   
def get_username_from_remote(remote):
    return remote.split('/')[-2]
    
def get_repo_name_from_remote(remote):
    return remote.split('/')[-1]

def get_host_from_remote(remote):
    return remote.split('/')[-3]
