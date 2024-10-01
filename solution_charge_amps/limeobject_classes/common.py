import limepkg_base_solution_helpers.common as base_common
import limepkg_basic_lead.translations as translations
from lime_application import LimeApplication
from lime_type import LimeObject
from lime_type.unit_of_work import UnitOfWork


def create_automated_flow_participant_history(
    participant: LimeObject,
    parent_object: LimeObject,
    uow: UnitOfWork,
) -> LimeObject:
    """Create a history note saying that a person has enrolled a specific flow.
    based on the relation of the automatedflowparticipant cards

    Args:
        participant (LimeObject): automatedflowparticipant limeobject
        parent_object (LimeObject): Limeobject to relate the history to
        uow (UnitOfWork): Unit of work to add the related objects to

    Returns:
        LimeObject: Created history note
    """
    app: LimeApplication = participant.application

    automatedflow: LimeObject = participant.properties.automatedflow.fetch()
    person: LimeObject = participant.properties.person.fetch()

    return base_common.add_history_from_object(
        limeobject=parent_object,
        history_type_key="autolog",
        note=translations.get_translation(
            app,
            "automatedflowparticipant.created.history.note",
            flow_name=automatedflow.properties.name.value,
            person_name=person.properties.name.value,
        ),
        uow=uow,
        attach_active_coworker=True,
        auto_relate=False,
    )
