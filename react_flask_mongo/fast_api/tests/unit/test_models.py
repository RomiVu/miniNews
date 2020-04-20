import pytest
from sqlalchemy.orm import selectinload, joinedload

from admin.db import User, Client, Tasks, TaskTypes, Permission, Role, Application


def test_add_user(db_session):
    user = User(username="loooke1", email="sdasfas@asds.com")
    user.set_password("123456lk@@")
    db_session.add(user)
    db_session.commit()
    row = db_session.query(User).filter(User.username == "loooke1").first()
    assert row.username == "loooke1"
    assert row.verify_password("123456lk@@")


@pytest.fixture(scope='function')
def get_client_app(db_session):
    clients = db_session.query(Client).order_by(Client.id)
    app = db_session.query(Application).filter_by(name="home").first()
    return clients, app


@pytest.fixture(scope='function')
def get_client_staff(db_session):
    users = db_session.query(User).order_by(User.id).all()
    client = db_session.query(Client).\
                    filter_by(organization="tencent").first()
    staff = client.staff
    return users, staff


def test_app_client(get_client_app, insert_full_data):
    clients, app = get_client_app
    assert app is not None
    for c in clients:
        if c.organization == "alibabab":
            assert c not in app.clients
        else:
            assert c in app.clients


def test_client_staff(get_client_staff, insert_full_data):
    users, staff = get_client_staff
    assert staff != []
    for u in users:
        if u.username in ["looooke2","looooke5","looooke6"]:
            assert u in staff
        else:
            assert u not in staff

def test_user_tasks(db_session, insert_full_data):
    u = db_session.query(User).filter_by(username="looooke9").first()
    tasks = db_session.query(Tasks).order_by(Tasks.id).all()

    for t in tasks:
        assert t in u.tasks
    
    u = db_session.query(User).filter_by(username="looooke8").first()
    assert u.tasks == []


def test_user_permission(db_session, insert_full_data):
    u1 = db_session.query(User).filter_by(username="looooke9").first()
    r1 = db_session.query(Role).filter_by(name="root").first()
    assert u1.role  == r1
    
    u2 = db_session.query(User).filter_by(username="looooke8").first()
    r2 = db_session.query(Role).filter_by(name="demo").first()
    assert u2.role == r2

    u3 = db_session.query(User).filter_by(username="looooke2").first()
    permissions = u3.role.permissions
    assert len(permissions) == 4

    for p in permissions:
        assert p.name != "read_limit"
        assert p.name != "api"


def test_user_permission_vaild(db_session, insert_full_data):
    u1 = db_session.query(User).filter_by(username="looooke9").first()
    u2 = db_session.query(User).filter_by(username="looooke1").first()
    u3 = db_session.query(User).filter_by(username="looooke3").first()

    assert u1.is_vaild()
    assert u2.is_vaild()
    assert u3.is_vaild()


def test_task_tasktype(db_session, insert_full_data):
    tp = db_session.query(TaskTypes).filter_by(name="education").first()
    assert len(tp.tasks) == 4
    for t in tp.tasks:
        assert t.url in ["http://tech.ifeng.com/", "http://finance.ifeng.com/",
                        "http://ent.ifeng.com/", "http://edu.ifeng.com/"]
