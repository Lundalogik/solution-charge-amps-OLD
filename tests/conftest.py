# The conftest.py file serves as a means of providing fixtures for an entire directory.
# You can find information about reusable lime-core fixtures here:
# https://platform.docs.lime-crm.com/en/latest/development/running-tests/#fixtures

from unittest.mock import MagicMock

import kombu
import pytest
from lime_event_handler.worker import Worker


@pytest.fixture
def kombu_connection():
    """A connection to an in-memory message queue"""
    connection = kombu.Connection("memory://")
    yield connection
    connection.release()


@pytest.fixture
def publisher(lime_app, kombu_connection):
    """A publisher function that posts to the in-memory queue"""
    exchange = kombu.Exchange(f"lime.{lime_app.identifier}", type="topic")
    producer = kombu.Producer(kombu_connection, exchange)

    def publish(routing_key, body):
        producer.publish(body, routing_key)

    return publish


@pytest.fixture
def worker(kombu_connection, lime_app, lime_databases):
    yield Worker(
        databases=lime_databases,
        connection=kombu_connection,
        applications=[lime_app.identifier],
    )


@pytest.fixture
def lime_app(lime_app, save_lime_objects, publisher):
    lime_app._publisher = publisher
    save_lime_objects(
        lime_app.limetypes.coworker(username=lime_app.user_id, firstname="Admin")
    )
    return lime_app


@pytest.fixture
def lime_app_non_admin(lime_app_non_admin, save_lime_objects, publisher):
    lime_app_non_admin._publisher = publisher
    save_lime_objects(
        lime_app_non_admin.limetypes.coworker(
            username=lime_app_non_admin.user_id, firstname="User"
        )
    )
    return lime_app_non_admin


@pytest.fixture
def no_registered_limeobjects(monkeypatch):
    """Ensure that we have no registered custom limeobjects for a test"""
    monkeypatch.setattr("lime_type.limetypes.limeobject_classes", {})


@pytest.fixture
def send_task(monkeypatch):
    class TaskMock:
        def __init__(self):
            self.id = "1"
            self.result = None
            self.status = "PENDING"

        def to_dict(self) -> dict:
            return {"id": self.id, "result": self.result, "status": self.status}

    send_task = MagicMock(return_value=TaskMock())

    monkeypatch.setattr("lime_task.send_task", send_task)

    return send_task
