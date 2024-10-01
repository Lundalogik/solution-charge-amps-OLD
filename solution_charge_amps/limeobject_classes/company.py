import logging

import limepkg_base_solution_helpers.common as base_common
import limepkg_base_solution_helpers.limeobject_classes.company as base_company
from lime_type import LimeObject

logger = logging.getLogger(__name__)


class Company(LimeObject):
    def before_update(self, uow, **kwargs):
        super().before_update(uow, **kwargs)

        base_common.add_history_if_option_change(
            limeobject=self,
            option_prop="buyingstatus",
            uow=uow,
        )

        if self.properties.phone.is_dirty():
            self.properties.phone.value = base_common.format_phone(
                self.properties.phone.value
            )
        base_company.set_full_visiting_address(self)
        base_company.set_full_postal_address(self)

    def before_delete(self, uow, **kwargs):
        super().before_delete(uow, **kwargs)

    def after_update(self, unsaved_self, **kwargs):
        super().after_update(unsaved_self, **kwargs)


def register_limeobject_classes(register_class):
    register_class("company", Company)
