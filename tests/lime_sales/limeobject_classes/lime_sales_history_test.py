import datetime
from typing import Callable, Dict, Iterable, List

import lime_type
import pytz
from lime_application import LimeApplication
from lime_type import LimeObject


def test_latestsalescontact_still_empty_when_non_salescontact_history_is_attached(
    lime_app: LimeApplication,
    save_lime_objects: Callable[[Iterable[LimeObject]], List[LimeObject]],
    loaded_plugins,
):
    data: Dict[str, LimeObject] = lime_type.create_limeobjects_from_dsl(
        lime_app.limetypes,
        """
        deal:
            deal1:
                name: good deal
        company:
            company1:
                name: nice company
        """,
    )
    deal = data["deal1"]
    company = data["company1"]

    test_date = datetime.datetime(2022, 2, 2, 22, 0, 0, tzinfo=pytz.UTC)

    # Make sure that relevant fields are empty
    assert deal.properties.latestsalescontact.value is None
    assert company.properties.latestsalescontact.value is None

    # Create a history note that isn't a sales contact
    # to make sure relevant fields are still empty
    history: LimeObject = lime_app.limetypes.history(
        note="nice note", type="comment", date=test_date.isoformat()
    )
    history.properties.deal.attach(deal)
    history.properties.company.attach(company)
    history, deal, company = save_lime_objects(history, deal, company)

    # Refreshes the limeobjects because the relevant fields
    # are handled in a separate uow in afterupdate
    deal: LimeObject = lime_app.limetypes.deal.get(deal.id)
    company: LimeObject = lime_app.limetypes.company.get(deal.id)

    assert deal.properties.latestsalescontact.value is None
    assert company.properties.latestsalescontact.value is None


def test_latestsalescontact_is_set_when_salescontact_history_is_attached(
    lime_app: LimeApplication,
    save_lime_objects: Callable[[Iterable[LimeObject]], List[LimeObject]],
    loaded_plugins,
):
    data: Dict[str, LimeObject] = lime_type.create_limeobjects_from_dsl(
        lime_app.limetypes,
        """
        deal:
            deal1:
                name: good deal
        company:
            company1:
                name: nice company
        """,
    )
    deal = data["deal1"]
    company = data["company1"]

    test_date = datetime.datetime(2022, 2, 2, 22, 0, 0, tzinfo=pytz.UTC)

    # Make sure that relevant field is empty
    assert deal.properties.latestsalescontact.value is None
    assert company.properties.latestsalescontact.value is None

    # Create a history note that is a sales contact
    # to make sure relevant fields are updated
    history: LimeObject = lime_app.limetypes.history(
        note="nice note", type="salescall", date=test_date.isoformat()
    )
    history.properties.deal.attach(deal)
    history.properties.company.attach(company)
    history, deal, company = save_lime_objects(history, deal, company)

    # Refreshes the limeobjects because the relevant fields
    # are handled in a separate uow in afterupdate
    deal: LimeObject = lime_app.limetypes.deal.get(deal.id)
    company: LimeObject = lime_app.limetypes.company.get(deal.id)

    assert (
        deal.properties.latestsalescontact.value.astimezone(pytz.UTC).isoformat()
        == test_date.isoformat()
    )
    assert (
        company.properties.latestsalescontact.value.astimezone(pytz.UTC).isoformat()
        == test_date.isoformat()
    )
