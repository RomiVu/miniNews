from datetime import datetime, timedelta
import sys
from os.path import dirname as d
from os.path import abspath, join
root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from admin import app
from admin.db import Base, User, Client, Tasks, TaskTypes, Permission, Role, Application

from admin.config import setting

@pytest.fixture(scope='module')
def test_client():
    client = TestClient(app)
    yield client

@pytest.fixture(scope='session')
def engine():
    db_url = setting.DATABASE_URL
    return create_engine(db_url)


@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def db_session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # begin the nested transaction
    # transaction = connection.begin()

    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    # transaction.rollback()

    # put back the connection to the connection pool
    connection.close()

@pytest.fixture(scope='module')
def insert_full_data(db_session):
    app1 = Application(name="admin", description="this is 1st app")
    app2 = Application(name="home", description="this is 2nd app")
    app3 = Application(name="api", description="this is 3rd app")

    c1 = Client(organization="alibabab")
    c2 = Client(organization="baidu")
    c3 = Client(organization="tencent")
    c4 = Client(organization="bytedance")

    app1.clients= [c1, c2]
    app2.clients = [c2, c3, c4]
    app3.clients.append(c2)

    r1 = Role(name="root")
    r2 = Role(name="admin")
    r3 = Role(name="staff")
    r4 = Role(name="demo")

    p1 = Permission(name="read_limit", description="limit content for vistors or demo")
    p2 = Permission(name="read")
    p3 = Permission(name="update")
    p4 = Permission(name="create")
    p5 = Permission(name="delete")
    p6 = Permission(name="api")


    r1.permissions = [p2,p3,p4,p5,p6]
    r2.permissions = [p2,p3,p4,p5]
    r3.permissions = [p2, p3]
    r4.permissions.append(p1)

    u0 = User(username="looooke9", email="yuxilvke9@gmail.com")
    u1 = User(username="looooke1", email="yuxil567vke1@gmail.com") 
    u2 = User(username="looooke2", email="yuxilvke2@gmail.com")
    u3 = User(username="looooke3", email="yuxilvke3@gmail.com")
    u4 = User(username="looooke4", email="yuxi123lasd3@gmail.com") 
    u5 = User(username="looooke5", email="yuxad7ke3@gmail.com") 
    u6 = User(username="looooke6", email="yadxiq54ewadsade3@gmail.com") 
    u7 = User(username="looooke7", email="yuas23dilvke3@gmail.com") 
    u8 = User(username="looooke8", email="yadsaq22d3@gmail.com") 

    r1.users = [u0]
    r2.users = [u1, u2, u3]
    r3.users = [u4, u5, u6, u7]
    r4.users = [u8]

    c1.staff = [u0, u8]
    c2.staff = [u1, u4]
    c3.staff = [u2, u5, u6]
    c4.staff = [u3, u7]

    t1 = Tasks(url="http://news.ifeng.com/")
    t2 = Tasks(url="http://tech.ifeng.com/")
    t3 = Tasks(url="http://finance.ifeng.com/")
    t4 = Tasks(url="http://sports.ifeng.com/")
    t5 = Tasks(url="http://ent.ifeng.com/")
    t6 = Tasks(url="http://edu.ifeng.com/")


    u0.tasks = [t1, t2, t3, t4, t5, t6]
    u1.tasks = [t2, t3, t4]
    u2.tasks = [t1, t2, t3]
    u3.tasks = [t4, t5]
    u4.tasks = [t3]
    u5.tasks = [t2, t5,]
    u6.tasks = [t6]
    u7.tasks = [t2, t3]
    #u8.tasks= []

    tp1 = TaskTypes(name="tech")
    tp2 = TaskTypes(name="entertainment")
    tp3 = TaskTypes(name="finance")
    tp4 = TaskTypes(name="e-commerce")
    tp5 = TaskTypes(name="balabal")
    tp6 = TaskTypes(name="education")

    tp1.tasks = [t1, t5]
    tp2.tasks = [t2]
    tp3.tasks = [t4, t5]
    tp6.tasks = [t2, t3, t5, t6]


    u0.set_password("nkfquwfskjfnskajn")
    u1.set_password("nkfquwfskjfnskajn")
    u2.set_password("nkfquwfskjfnskajn")
    u3.set_password("nkfquwfskjfnskajn")

    db_session.add_all([app1,app2, app3])
    
    db_session.add_all([c1, c2, c3, c4])
    db_session.add_all([r1, r2, r3, r4])
    db_session.add_all([p1, p2, p3, p4, p5, p6])

    db_session.add_all([u0, u1, u2, u3, u4, u5, u6, u7, u8])
    db_session.add_all([t1, t2, t3, t4, t5, t6])
    db_session.add_all([tp1, tp2, tp3, tp4, tp5, tp6])

    db_session.commit()


    