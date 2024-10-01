from typing import Callable, Iterable, List

import addon_lime_automation.sdk as automation_sdk
import lime_type
import limepkg_base_solution_helpers.common as base_common
import mock
from lime_application import LimeApplication
from lime_type import LimeObject


def test_trigger_automatedflow(
    lime_app: LimeApplication,
    save_lime_objects: Callable[[Iterable[LimeObject]], List[LimeObject]],
    loaded_plugins,
):
    data = lime_type.create_limeobjects_from_dsl(
        lime_app.limetypes,
        """
        lead:
            lead1:
                description: good company
                leadstatus: new
                person: person1
                automatedflow: automatedflow1
        automatedflow:
            automatedflow1:
                name: good flow
        person:
            person1:
                firstname: good
                lastname: person
                name: good person
        """,
    )
    automatedflow: LimeObject = data["automatedflow1"]
    person: LimeObject = data["person1"]

    # Mocked participant returned by the patched "AutomatedFlowParticipantFactory"
    dummy_participant = lime_app.limetypes.automatedflowparticipant()
    dummy_participant.properties.automatedflow.attach(automatedflow)
    dummy_participant.properties.person.attach(person)

    lead: LimeObject = data["lead1"]
    lead.properties.leadstatus.set_by_key("qualify")

    factory_mock = mock.MagicMock()
    init_participant_function = mock.MagicMock(
        return_value=[
            dummy_participant,
            person,
            automatedflow,
        ]
    )
    factory_mock.init_automatedflow_participant = init_participant_function

    # Mock the "AutomatedFlowParticipantFactory"
    # because we don't want to test it's logic
    # just the arguments passed to it
    with mock.patch.object(
        automation_sdk,
        "AutomatedFlowParticipantFactory",
        side_effect=lambda *args, **kwargs: factory_mock,
    ):
        # Mock the "check_duplicate" because we don't want to test it's logic
        # just the arguments passed to it
        with mock.patch.object(
            base_common,
            "check_duplicate",
            side_effect=lambda *args, **kwargs: False,
        ) as mockedDuplicate:
            # Save the lead
            lead = next(iter(save_lime_objects(lead)))

    try:
        automated_flow_participant = next(
            lead.properties.automatedflowparticipant.fetch()
        )
        assert (
            automated_flow_participant.properties.person.value
            == dummy_participant.properties.person.value
        )
        assert (
            automated_flow_participant.properties.automatedflow.value
            == dummy_participant.properties.automatedflow.value
        )

        # Check calls and arguments on init_automatedflow_participant
        init_participant_function.assert_called_once()
        call_kwargs = init_participant_function.call_args.kwargs
        assert len(call_kwargs) == 2
        assert automatedflow.compare_to(call_kwargs["automatedflow"])
        assert person.compare_to(call_kwargs["related_object"])

        # Check calls and arguments on check_duplicate
        mockedDuplicate.assert_called_once()
        call_kwargs = mockedDuplicate.call_args.kwargs
        assert len(call_kwargs) == 3
        assert isinstance(call_kwargs["object_to_create"], LimeObject)
        assert (
            call_kwargs["object_to_create"].limetype.name
            == automated_flow_participant.limetype.name
        )
        assert call_kwargs["properties_to_check"] == [
            dummy_participant.properties.automatedflow,
            dummy_participant.properties.person,
        ]
        assert call_kwargs["static_criterias"] == [
            {
                "key": "bw_status",
                "op": "IN",
                "exp": ["initialize", "inprogress"],
            }
        ]

    except StopIteration:
        assert False, "The lead should have a automatedflowparticipant related"
