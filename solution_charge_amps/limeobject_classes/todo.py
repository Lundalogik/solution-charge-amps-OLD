import logging

import limepkg_basic_deal.decorators as deal_decorators
from lime_type import LimeObject

logger = logging.getLogger(__name__)


@deal_decorators.todo()
class Todo(LimeObject):
    def before_update(self, uow, **kwargs):
        super().before_update(uow, **kwargs)

    def before_delete(self, uow, **kwargs):
        super().before_delete(uow, **kwargs)

    def after_update(self, unsaved_self, **kwargs):
        super().after_update(unsaved_self, **kwargs)


def register_limeobject_classes(register_class):
    register_class("todo", Todo)
