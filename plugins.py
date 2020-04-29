import apps
from core import Window
import importlib
import pkgutil


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


builtin_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(apps)
}

thirdparty_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('pyImguiOs_')
}

def get_app_list(cls=Window):
    for i in cls.__subclasses__():
        if i.inAppMenu:
            yield i
        yield from get_app_list(i)
