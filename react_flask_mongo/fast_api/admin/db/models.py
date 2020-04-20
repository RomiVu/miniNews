from datetime import datetime, timedelta

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256

from .connect import Base

client_apps = Table(
    "client_apps", Base.metadata,
    Column("app_id", ForeignKey("application.id"), primary_key=True),
    Column("client_id", ForeignKey("clients.id"), primary_key=True)
)

task_users = Table(
    "task_users", Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id"), primary_key=True)
)

permission_role = Table(
    "permission_role", Base.metadata,
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True)
)

tasks_types = Table(
    "tasks_types", Base.metadata,
    Column("tasks", ForeignKey("tasks.id"), primary_key=True),
    Column("tasktypes", ForeignKey("tasktypes.id"), primary_key=True)
)


def default_vaild_time(cls):
    return datetime.utcnow() + timedelta(minutes=60)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String(11))
    password_hash = Column(String)
    vaild_before = Column(DateTime, default=default_vaild_time)
    last_seen = Column(DateTime, default=datetime.utcnow)

    client_id = Column(Integer, ForeignKey("clients.id"))
    role_id = Column(Integer, ForeignKey("role.id"))

    role = relationship("Role", back_populates="users")
    tasks = relationship('Tasks',
                          secondary=task_users,
                          back_populates="users"
                        )
    company = relationship("Client", back_populates="staff")

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)
    
    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def is_vaild(self):
        return self.vaild_before > datetime.utcnow()

    def __repr__(self):
        return f"<User id:{self.id} name:{self.username}>"

class OAuthUser(Base):
    __tablename__ = "oauth_user"

    id = Column(String, primary_key=True)
    oauth_name = Column(String, index=True, nullable=False)
    access_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    refresh_token = Column(String, nullable=True)
    user_email = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    organization = Column(String(50), unique=True)
    address = Column(String(120))
    remark =  Column(String(120))
    created_time = Column(DateTime, default=datetime.utcnow)

    staff = relationship("User", 
                          back_populates="company",
                          lazy="select", 
                          cascade="all, delete, delete-orphan"
                        )
    apps = relationship("Application", secondary=client_apps, back_populates="clients")

    def __repr__(self):
        return f"<Client id:{self.id} name:{self.organization}>"

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(512), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    added_time = Column(DateTime, default=datetime.utcnow)
    modify_time = Column(DateTime)
    priority = Column(Integer)
    description = Column(String(140))
    schedule_time = Column(DateTime)
    interval =  Column(Integer)

    users = relationship("User", secondary=task_users, back_populates="tasks")
    task_type = relationship("TaskTypes", secondary=tasks_types, back_populates="tasks")

    def __repr__(self):
        return f"<Tasks id:{self.id} url:{self.url}>"


class TaskTypes(Base):
    __tablename__ = "tasktypes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True)
    description = Column(String(140))

    tasks = relationship("Tasks", secondary=tasks_types, back_populates="task_type")

    def __repr__(self):
        return f"<TaskType id:{self.id} name:{self.name}>"
   

class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True)
    description = Column(String(120))

    roles = relationship("Role", secondary=permission_role, back_populates="permissions")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True)
    description = Column(String(120))

    permissions = relationship("Permission",secondary=permission_role,back_populates="roles")
    users = relationship("User", back_populates="role", lazy="dynamic")


class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), index=True, unique=True)
    description = Column(String(120))
    created_time = Column(DateTime, default=datetime.utcnow)

    clients = relationship("Client",
                            secondary=client_apps,
                            back_populates="apps")


