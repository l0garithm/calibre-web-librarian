import os
import re
import sys
import json
from packaging.requirements import Requirement

from .constants import BASE_DIR
try:
    from importlib.metadata import version
    importlib = True
    ImportNotFound = BaseException
except ImportError:
    importlib = False
    version = None

if not importlib:
    try:
        import pkg_resources
        from pkg_resources import DistributionNotFound as ImportNotFound
        pkgresources = True
    except ImportError as e:
        pkgresources = False


def load_dependencies(optional=False):
    deps = []
    if optional:
        dep_file = os.path.join(BASE_DIR, 'optional-requirements.txt')
    else:
        dep_file = os.path.join(BASE_DIR, 'requirements.txt')
    with open(dep_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    req = Requirement(line)
                    # Extract relevant information from req object
                    name = req.name
                    specifier = str(req.specifier) if req.specifier else None
                    url = req.url
                    extras = ','.join(req.extras) if req.extras else None
                    deps.append([name, specifier, url, extras])
                except Exception as e:
                    print(f"Warning: Unable to parse requirement '{line}': {e}")
    return deps


from importlib.metadata import version, PackageNotFoundError

def get_installed_version(package_name):
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Not installed"

def dependency_check(optional=False):
    d = []
    deps = load_dependencies(optional)
    for dep in deps:
        name, specifier, url, extras = dep
        
        if url:
            d.append({
                'name': name,
                'target': "from URL",
                'found': "URL-based dependency"
            })
            continue
        
        installed_version = get_installed_version(name)
        
        if not specifier:
            d.append({
                'name': name,
                'target': "any",
                'found': installed_version
            })
            continue
        
        d.append({
            'name': name,
            'target': specifier,
            'found': installed_version
        })
    
    return d
