# -*- coding: utf-8 -*-

"""Top-level package for Leginorma."""

__author__ = "Rémi Delbouys"
__email__ = "remi.delbouys@laposte.net"
# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "0.0.0"


def get_module_version():
    return __version__


from .api import LegifranceClient, LegifranceRequestError  # noqa: F401
from .models import ArticleStatus, LegifranceArticle, LegifranceSection, LegifranceText  # noqa: F401
