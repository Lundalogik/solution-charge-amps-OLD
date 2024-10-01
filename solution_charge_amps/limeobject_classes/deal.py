import datetime
import logging
from typing import Optional

import limepkg_base_solution_helpers.common as base_common
import limepkg_base_solution_helpers.limeobject_classes.general as base_general
import limepkg_basic_deal.decorators as deal_decorators
from lime_type import LimeObject
from lime_type.unit_of_work import UnitOfWork

import solution_charge_amps.limeobject_classes.common as common

logger = logging.getLogger(__name__)


@deal_decorators.deal()
class Deal(LimeObject):
    def before_update(self, uow: UnitOfWork, **kwargs):
        super().before_update(uow, **kwargs)

        if base_general.option_changed(self, "dealstatus", to_key=["agreement"]):
            self.properties.expecteddate.value = datetime.datetime.now()

        base_common.add_history_if_option_change(
            limeobject=self,
            option_prop="dealstatus",
            uow=uow,
        )
        created_from_lead = _get_created_from_lead(self, uow)
        if self.is_new and created_from_lead:
            _create_automated_flow_participant_history(
                self,
                created_from_lead,
                uow,
            )

    def before_delete(self, uow, **kwargs):
        super().before_delete(uow, **kwargs)

    def after_update(self, unsaved_self, **kwargs):
        super().after_update(unsaved_self, **kwargs)


def register_limeobject_classes(register_class):
    register_class("deal", Deal)


def _create_automated_flow_participant_history(
    deal: LimeObject,
    lead: LimeObject,
    uow: UnitOfWork,
):
    """Fetch all flow participants related to the lead
    and create a history on each dated to the particpant created time

    Args:
        deal (LimeObject): Deal to attach history to
        lead (LimeObject): Lead to fetch participants from
        uow (UnitOfWork): Unit of work to add all relations to
    """
    if not lead.get_property("automatedflowparticipant"):
        return

    automated_flow_participants = lead.properties.automatedflowparticipant.fetch()

    for participant in automated_flow_participants:
        history = common.create_automated_flow_participant_history(
            participant,
            deal,
            uow,
        )
        history.properties.date.value = participant.createdtime


def _get_created_from_lead(deal: LimeObject, uow: UnitOfWork) -> Optional[LimeObject]:
    """Fetch a lead from the uow that is related to the current deal.

    Args:
        deal (LimeObject): Deal object that should be related to the lead
        uow (UnitOfWork): Unit of work to fetch the lead from

    Returns:
        Optional[LimeObject]: The lead, if found, else None
    """

    def _get_idx(obj: LimeObject):
        if hasattr(obj, "idx"):
            return obj.idx

    deal_idx = _get_idx(deal)

    if deal_idx is None:
        return

    return next(
        (
            ci.unsaved
            for ci in uow.context.get_all()
            if ci.unsaved.limetype.name == "lead"
            and _get_idx(ci.unsaved.properties.deal.fetch()) == deal_idx
        ),
        None,
    )
