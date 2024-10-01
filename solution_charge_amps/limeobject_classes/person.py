import logging

import limepkg_base_solution_helpers.common as base_common
import limepkg_base_solution_helpers.limeobject_classes.general as base_general
from lime_type import LimeObject

logger = logging.getLogger(__name__)


class Person(LimeObject):
    def before_update(self, uow, **kwargs):
        super().before_update(uow, **kwargs)

        base_general.set_name_from_firstname_lastname(self)

        if self.properties.phone.is_dirty():
            self.properties.phone.value = base_common.format_phone(
                self.properties.phone.value
            )
        if self.properties.mobilephone.is_dirty():
            self.properties.mobilephone.value = base_common.format_phone(
                self.properties.mobilephone.value
            )

    def before_delete(self, uow, **kwargs):
        super().before_delete(uow, **kwargs)

    def after_update(self, unsaved_self, **kwargs):
        super().after_update(unsaved_self, **kwargs)


def register_limeobject_classes(register_class):
    register_class("person", Person)
