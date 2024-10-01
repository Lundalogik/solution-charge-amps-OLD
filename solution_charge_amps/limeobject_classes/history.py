import logging

import lime_errors
import lime_filter
import limepkg_base_solution_helpers.limeobject_classes.general as base_general
from lime_type import LimeType
from lime_type.limeobjects import BelongsToPropertyAccessor, LimeObject
from lime_type.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class History(LimeObject):
    def before_update(self, uow, **kwargs):
        super().before_update(uow, **kwargs)

    def before_delete(self, uow, **kwargs):
        super().before_delete(uow, **kwargs)

    def after_update(self, unsaved_self, **kwargs):
        super().after_update(unsaved_self, **kwargs)

        uow = self.application.unit_of_work()
        if (
            unsaved_self.is_new
            or base_general.option_changed(
                unsaved_self, "type", to_key=["salescall", "customervisit"]
            )
            or base_general.option_changed(
                unsaved_self, "type", from_key=["salescall", "customervisit"]
            )
            or unsaved_self.properties.date.is_dirty()
        ):
            _set_latestsalescontact(self, unsaved_self, "deal", uow)
            _set_latestsalescontact(self, unsaved_self, "company", uow)
        else:
            if unsaved_self.properties.deal.is_dirty():
                _set_latestsalescontact(self, unsaved_self, "deal", uow)
            if unsaved_self.properties.company.is_dirty():
                _set_latestsalescontact(self, unsaved_self, "company", uow)

        uow.commit()


def register_limeobject_classes(register_class):
    register_class("history", History)


def _set_latestsalescontact(
    history: History,
    unsaved_history: History,
    relation_prop_name: str,
    uow: UnitOfWork,
):
    """Set latestsalescontact on the given relate property name.
    Handles both current related object and the previous related object.

    Args:
        history (History): History object
        unsaved_history (History): The unsaved history object
        relation_prop_name (LimeObject): The unsaved history object
        uow (UnitOfWork): Unit of work to use
    """
    type_option_mapper = {o.key: o.id for o in history.properties.type.options}

    def _handle_sales_contact_on_object(parent_object: LimeObject):
        if not parent_object:
            return

        latest_salescontact = base_general.get_latest_or_oldest_object_on_relation(
            parent_object=parent_object,
            relation_prop_name="history",
            date_property_name="date",
            static_criterias=[
                lime_filter.InOperator(
                    "type",
                    [
                        type_option_mapper["salescall"],
                        type_option_mapper["customervisit"],
                    ],
                )
            ],
        )

        parent_object.properties.latestsalescontact.value = (
            latest_salescontact.properties.date.value if latest_salescontact else None
        )
        uow.add(parent_object)

    relation_prop: BelongsToPropertyAccessor = history.get_property(relation_prop_name)
    parent_object: LimeObject = relation_prop.fetch()

    _handle_sales_contact_on_object(parent_object)

    # Handle the previous deals latest salescontact
    unsaved_relation_prop: BelongsToPropertyAccessor = unsaved_history.get_property(
        relation_prop_name
    )

    if unsaved_relation_prop.is_dirty():
        try:
            lime_type: LimeType = unsaved_relation_prop.get_related_limetype()
            prev_parent_object = lime_type.get(unsaved_relation_prop.original_value)
            _handle_sales_contact_on_object(prev_parent_object)
        except lime_errors.NotFoundError:
            pass  # Ignore if the previous object is not found
