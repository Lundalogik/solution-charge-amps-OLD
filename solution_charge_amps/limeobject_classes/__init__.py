import importlib
import logging
import pkgutil

logger = logging.getLogger(__name__)


def register_limeobject_classes(register_func):
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
        if module_name.endswith("_test"):
            continue
        module_fullname = f"{__name__}.{module_name}"
        logger.info("Loading %s", module_fullname)
        module = importlib.import_module(module_fullname)

        if hasattr(module, "register_limeobject_classes"):
            module.register_limeobject_classes(register_func)
