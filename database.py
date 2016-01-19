# coding: utf-8

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool


def config(config_name):
    module = __import__('config.{0}'.format(config_name),
                        fromlist=[config_name])
    return module


_Base = declarative_base()


class SessionProxy:
    """
    with 上下文代理

    1.create scoped_session
    2.拿 session 做xxx业务
    3.session.remove
    """
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        self._session = scoped_session(self.session)
        return self._session

    def __exit__(self, type, value, trace):
        self._session.remove()


class Base(_Base):
    """
    公用 model
    """
    __abstract__ = True

    @classmethod
    def query(cls, session):
        """
        数据库查询方法.
        cls.query == session.query(cls)
        :param session: SQLALCHEMY().session
        :return: session.query(cls)
        """
        return session.query(cls)


def get_engine(config_name=None):
    """
    Creates engine.
    :param config_name: 配置文件 config_name.py
    :return: engine
    """
    if config_name == None:
        config_name = 'development'
    print(config_name)
    uri = config(config_name).SQLALCHEMY_DATABASE_URI
    _engine = create_engine(uri, echo=True, poolclass=QueuePool)
    return _engine


class SQLALCHEMY():
    """
    SQLALCHEMY 类.
    获取参数 config_name 创建数据库.
    """
    def __init__(self, config_name=None):
        self.engine = get_engine(config_name)
        self.Session = sessionmaker(bind=self.engine)

    @property
    def session(self):
        return SessionProxy(self.Session)

    def create_all(self):
        '''
        在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在元数据上。
        否则你就必须在调用 SQLAlchemy() 之前导入它们。
        '''
        from app import models
        Base.metadata.create_all(bind=self.engine)

    def drop_all(self):
        """
        在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在元数据上。
        否则你就必须在调用 SQLAlchemy() 之前导入它们。
        """
        from app import models
        Base.metadata.drop_all(bind=self.engine)
