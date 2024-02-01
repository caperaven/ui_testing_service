import os
import re


def get_os_path(path):
    path_components = re.split(r'[\\/]+', path)
    cross_platform_path = os.path.join(*path_components)

    if cross_platform_path.startswith("~/"):
        cross_platform_path = os.path.expanduser(cross_platform_path)

    return cross_platform_path
