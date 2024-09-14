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


def dependency_check(optional=False):
    d = list()
    dep_version_int = None
    low_check = None
    deps = load_dependencies(optional)
    for dep in deps:
        try:
            dep_version_int = [int(x) if x.isnumeric() else 0 for x in dep[0].split('.')]
            low_check = [int(x) for x in dep[3].split('.')]
            high_check = [int(x) for x in dep[5].split('.')]
        except AttributeError:
            high_check = []
        except ValueError:
            d.append({'name': dep[1],
                      'target': "available",
                      'found': "Not available"
                      })
            continue

        if dep[2].strip() == "==":
            if dep_version_int != low_check:
                d.append({'name': dep[1],
                          'found': dep[0],
                          "target": dep[2] + dep[3]})
                continue
        elif dep[2].strip() == ">=":
            if dep_version_int < low_check:
                d.append({'name': dep[1],
                          'found': dep[0],
                          "target": dep[2] + dep[3]})
                continue
        elif dep[2].strip() == ">":
            if dep_version_int <= low_check:
                d.append({'name': dep[1],
                          'found': dep[0],
                          "target": dep[2] + dep[3]})
                continue
        if dep[4] and dep[5]:
            if dep[4].strip() == "<":
                if dep_version_int >= high_check:
                    d.append(
                        {'name': dep[1],
                         'found': dep[0],
                         "target": dep[4] + dep[5]})
                    continue
            elif dep[4].strip() == "<=":
                if dep_version_int > high_check:
                    d.append(
                        {'name': dep[1],
                         'found': dep[0],
                         "target": dep[4] + dep[5]})
                    continue
    return d
