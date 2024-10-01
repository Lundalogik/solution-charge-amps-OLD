import logging

import limepkg_base_solution_helpers.common as base_common
import limepkg_smh_translations.translations as translations
from lime_application import LimeApplication
from lime_file import File
from lime_type import LimeObject
from lime_type.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


class Document(LimeObject):
    def before_update(self, uow, **kwargs):
        super().before_update(uow, **kwargs)

        if self.is_new:
            _create_document_history(self, uow)

    def before_delete(self, uow, **kwargs):
        super().before_delete(uow, **kwargs)

    def after_update(self, unsaved_self, **kwargs):
        super().after_update(unsaved_self, **kwargs)


def register_limeobject_classes(register_class):
    register_class("document", Document)


def _create_document_history(document: Document, uow: UnitOfWork):
    """Create history informing that a document was created

    Args:
        document (Document): Document to attach history to.
        uow (UnitOfWork): Unit of work to add relations to
    """
    app: LimeApplication = document.application
    document_file: File = document.properties.document.fetch()
    document_name = document_file.filename if document_file else ""

    coworker_name = app.coworker.properties.name.value if app.coworker else ""

    base_common.add_history_from_object(
        limeobject=document,
        history_type_key="autolog",
        note=translations.get_translation(
            app,
            "document.autohistory.note",
            document_name=document_name,
            coworker_name=coworker_name,
        ),
        uow=uow,
        attach_active_coworker=True,
        auto_relate=False,
    )
