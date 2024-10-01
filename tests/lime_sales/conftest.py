import lime_config
import lime_plugins
import lime_test.common.fixtures  # noqa
import lime_type
import pytest
from lime_application import LimeApplication

from tests.custom_dsl import dsl

# Force the lime_test database fixture to be used
database = lime_test.common.fixtures.database


@pytest.fixture
def lime_types():
    return lime_type.create_limetypes_from_dsl(dsl)


@pytest.fixture
def lime_app(lime_app) -> LimeApplication:
    lime_app.unit_of_work()

    coworker = lime_app.limetypes.coworker(
        firstname="Admin",
        lastname="Istrator",
        name="Admin Istrator",
        username=lime_app.user.id,
        _from_row=True,
    )

    uow = lime_app.unit_of_work()
    idx = uow.add(coworker)
    res = uow.commit()

    lime_app._coworker = res.get(idx)
    return lime_app


@pytest.fixture
def loaded_plugins(no_registered_limeobjects):
    return lime_plugins.load_plugins(config=lime_config.config)
