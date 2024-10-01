from typing import Callable, Iterable, List

import lime_type
from lime_application import LimeApplication
from lime_type import LimeObject


def test_expecteddate_when_setting_status_to_non_closed_status(
    lime_app: LimeApplication,
    save_lime_objects: Callable[[Iterable[LimeObject]], List[LimeObject]],
    loaded_plugins,
):
    data = lime_type.create_limeobjects_from_dsl(
        lime_app.limetypes,
        """
        deal:
            deal1:
                name: good deal
                dealstatus: contact
        """,
    )

    # Make sure it doesn't change expecteddate if changing to a non closed status
    deal: LimeObject = data["deal1"]
    deal.properties.dealstatus.set_by_key("requirement")
    deal = next(iter(save_lime_objects(deal)))

    assert deal.properties.expecteddate.value is None


def test_expecteddate_when_setting_status_to_closed_status(
    lime_app: LimeApplication,
    save_lime_objects: Callable[[Iterable[LimeObject]], List[LimeObject]],
    loaded_plugins,
):
    data = lime_type.create_limeobjects_from_dsl(
        lime_app.limetypes,
        """
        deal:
            deal1:
                name: good deal
                dealstatus: contact
        """,
    )

    # Make sure it doesn't change expecteddate if changing to a non closed status
    deal: LimeObject = data["deal1"]
    deal.properties.dealstatus.set_by_key("agreement")
    deal = next(iter(save_lime_objects(deal)))

    assert deal.properties.expecteddate.value
