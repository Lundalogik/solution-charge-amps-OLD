import logging
from typing import Optional

import addon_lime_automation.sdk as automation_sdk
import addon_lime_automation.sdk.decorators as automation_decorators
import limepkg_base_solution_helpers.common as base_common
import limepkg_basic_lead.decorators as lead_decorators
from lime_type import LimeObject
from lime_type.unit_of_work import UnitOfWork

import solution_charge_amps.limeobject_classes.common as common

logger = logging.getLogger(__name__)


@automation_decorators.automated_flow_decider()
@lead_decorators.lead()
class Lead(LimeObject):
    def before_update(self, uow: UnitOfWork, **kwargs):
        super().before_update(uow, **kwargs)

        base_common.add_history_if_option_change(
            limeobject=self,
            option_prop="leadstatus",
            uow=uow,
        )
        created_participant = _create_automated_flow_participant(self, uow)
        if created_participant:
            common.create_automated_flow_participant_history(
                created_participant,
                self,
                uow,
            )

    def before_delete(self, uow, **kwargs):
        super().before_delete(uow, **kwargs)

    def after_update(self, unsaved_self, **kwargs):
        super().after_update(unsaved_self, **kwargs)


def register_limeobject_classes(register_class):
    register_class("lead", Lead)


def _create_automated_flow_participant(
    lead: Lead,
    uow: UnitOfWork,
) -> Optional[LimeObject]:
    """Create automated flow participant
    if leadstatus have changed to qualify or convert and
    the lead is related to a person and automatedflow

    Args:
        lead (Lead): Lead object
        uow (UnitOfWork): Unit of work to add objects to

    Returns:
        Optional[LimeObject]:
        The potentially created automatedflowparticipant object
    """
    prop_status = lead.properties.leadstatus
    if not prop_status.is_dirty() or prop_status.value.key not in [
        "convert",
        "qualify",
    ]:
        return
    if not lead.get_property("automatedflow"):
        return

    factory = automation_sdk.AutomatedFlowParticipantFactory(lead.application)
    flow = lead.properties.automatedflow.fetch()
    person = lead.properties.person.fetch()
    if not flow or not person:
        return

    participant, *affected_objects = factory.init_automatedflow_participant(
        automatedflow=flow, related_object=person
    )
    will_be_duplicate = base_common.check_duplicate(
        object_to_create=participant,
        properties_to_check=[
            participant.properties.automatedflow,
            participant.properties.person,
        ],
        static_criterias=[
            {
                "key": "bw_status",
                "op": "IN",
                "exp": ["initialize", "inprogress"],
            }
        ],
    )
    if will_be_duplicate:
        return

    participant.properties.lead.attach(lead)

    uow.add(participant)
    for affected_object in affected_objects:
        uow.add(affected_object)

    return participant
