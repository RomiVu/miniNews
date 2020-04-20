import pytest
from sqlalchemy.orm import selectinload, joinedload

from admin.db import User, Client, Tasks, TaskTypes, Permission, Role, Application


@pytest.fixture(scope='function')
def init_auth_data(db_session):
    u0 = User(username="looooke9", email="yuxilvke9@gmail.com")
    u1 = User(username="looooke1", email="yuxil567vke1@gmail.com") 
    u2 = User(username="looooke2", email="yuxilvke2@gmail.com")
    u3 = User(username="looooke3", email="yuxilvke3@gmail.com")
    u4 = User(username="looooke4", email="yuxi123lasd3@gmail.com") 
    u5 = User(username="looooke5", email="yuxad7ke3@gmail.com") 
    u6 = User(username="looooke6", email="yadxiq54ewadsade3@gmail.com") 
    u7 = User(username="looooke7", email="yuas23dilvke3@gmail.com") 
    u8 = User(username="looooke8", email="yadsaq22d3@gmail.com") 

    u0.set_password("nkfquwfskjfnskajn")
    u1.set_password("nkfquwfskjfnskajn")
    u2.set_password("nkfquwfskjfnskajn")
    u3.set_password("nkfquwfskjfnskajn")

    db_session.add_all([u0, u1, u2, u3, u4, u5, u6, u7, u8])

    db_session.commit()


def test_login(test_client, init_auth_data):
    response = test_client.get('/login')
    assert response.status_code == 405

    response  = test_client.post('/login',
                                json={
                                    "username":"looooke9", 
                                    "password"="nkfquwfskjfnskajn"
                                    }
                                )

    assert response.status_code == 401
    assert response.json() == {"msg":"incorrect username or password"}


    response  = test_client.post('/login',
                                json={
                                    "username":"looooke9", 
                                    "password"="nkfquwfskjfnskajn"
                                    }
                                )

    assert response.status_code == 200
    assert response.json() == {"to be settled":" . . . "}

              
def test_register(test_client):
    response  = test_client.post('/register',
                                json={
                                    "username":"looooke9",
                                    "emai":"sdsda@asdas.com",
                                    "password"="nkfquwfskjfnskajn"
                                    }
                                )

    assert response.status_code == 401
    assert response.json() == {"msg":"email already existed"}


    response  = test_client.post('/register',
                                json={
                                    "username":"looooke9",
                                    "emai":"sdsd12342dsdsa@gmail.com",
                                    "password"="nkfquwfskjfnskajn"
                                    }
                                )

    assert response.status_code == 200
    assert response.json() == {"to be settled":" . . . "}
                            
def test_logout(test_client):
    response  = test_client.get('/logout')

    assert response.status_code == 200
    assert response.json() == {"to be settled":" . . . "}


def test_setting(test_client):
    response = test_client.post('/setting',
                                json={
                                    "username":"dasdsd",
                                    "password":"sdsdsdsds",
                                    "email":"sdasas@ads.com"
                                })
    assert response.status_code == 200
    assert response.json() == {"to be settled":" . . . "}
