import asyncio
import pytest
import pytest_asyncio

from motor import motor_asyncio
from testcontainers.mongodb import MongoDbContainer

from databases import users_mongo_client as mongo_client


mongo = MongoDbContainer()
collection_name = 'test_users'
collection: motor_asyncio.AsyncIOMotorCollection | None = None


@pytest_asyncio.fixture(scope='module', loop_scope='module', autouse=True)
async def setup_container(request: pytest.FixtureRequest):
    global collection
    loop = asyncio.get_event_loop()
    mongo.start()

    def remove_container():
        mongo.stop()

    request.addfinalizer(remove_container)
    mongo_client.connect_to_mongo_collection(mongo.username,
                                             mongo.password,
                                             mongo.get_container_host_ip(),
                                             mongo.get_exposed_port(mongo.port),
                                             mongo.dbname,
                                             collection_name,
                                             loop)
    uri = (f'mongodb://{mongo.username}:{mongo.password}@'
           f'{mongo.get_container_host_ip()}:{mongo.get_exposed_port(mongo.port)}')
    client: motor_asyncio.AsyncIOMotorClient = motor_asyncio.AsyncIOMotorClient(uri, io_loop=loop)
    collection = client[mongo.dbname][collection_name]


@pytest_asyncio.fixture(loop_scope='module', autouse=True)
async def setup_data():
    await asyncio.sleep(0.5)
    await collection.drop()


@pytest.mark.asyncio(loop_scope='module')
async def test_create_user():
    user_id = 1
    user_name = 'Dummy'

    await mongo_client.add_user(user_id, user_name)
    docs_count = await collection.count_documents({})

    assert docs_count == 1

    user_doc = await collection.find_one({'_id': user_id})

    assert user_doc['name'] == user_name
    assert user_doc["registration_finished"] is False
    assert user_doc["timetable"] == []


@pytest.mark.asyncio(loop_scope='module')
async def test_add_user_and_get_by_id():
    await mongo_client.add_user(100, "Test User")

    user = await mongo_client.get_user_fields_by_id(100)
    assert user is not None
    assert user["_id"] == 100
    assert user["name"] == "Test User"
    assert user["registration_finished"] is False
    assert user["timetable"] == []


@pytest.mark.asyncio(loop_scope='module')
async def test_get_user_fields_by_name_with_projection():
    await mongo_client.add_user(102, "Selective User")

    user = await mongo_client.get_user_fields_by_name("Selective User", fields=["_id"])
    assert user is not None
    assert "_id" in user
    assert "name" not in user


@pytest.mark.asyncio(loop_scope='module')
async def test_update_only_name():
    await mongo_client.add_user(103, "Name A")
    await mongo_client.update_user(103, user_name="Name B")

    user = await mongo_client.get_user_fields_by_id(103)
    assert user["name"] == "Name B"
    assert user["registration_finished"] is False


@pytest.mark.asyncio(loop_scope='module')
async def test_update_user_name_and_timetable():
    update_user_name = "New Name"
    update_tt = [[1100, 1500]]
    await mongo_client.add_user(101, "Old Name")
    await mongo_client.update_user(101, user_name=update_user_name, timetable=update_tt)

    user = await mongo_client.get_user_fields_by_id(101)
    assert user["name"] == update_user_name
    assert user["timetable"] == update_tt
    assert user["registration_finished"] is True
