from typing import Callable, Iterable, List

from lime_application import LimeApplication
from lime_type import LimeObject


def test_create_autolog_history_when_new(
    lime_app: LimeApplication,
    save_lime_objects: Callable[[Iterable[LimeObject]], List[LimeObject]],
    loaded_plugins,
):
    document: LimeObject = lime_app.limetypes.document(
        comment="nice document", type="document"
    )

    document = next(iter(save_lime_objects(document, application=lime_app)))

    try:
        history = next(document.properties.history.fetch())
        assert history.properties.note.value == (
            "limepkg_smh_translations.document.autohistory.note"
        )
        assert history.properties.type.value.key == "autolog"
        assert history.properties.coworker.value == lime_app.coworker.id
    except StopIteration:
        assert False, "history should be in the uow"
