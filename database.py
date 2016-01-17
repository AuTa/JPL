# coding: utf-8

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def config(config_name):
    module = __import__('config.{0}'.format(config_name), fromlist=[config_name])
    return module


Base = declarative_base()


def get_engine(config_name=None):
    """Creates engine."""
    if config_name == None:
        config_name = 'development'
    print(config_name)
    uri = config(config_name).SQLALCHEMY_DATABASE_URI
    _engine = create_engine(uri)
    return _engine

def create_scoped_session(engine=None, config_name=None):
    if engine is None:
        engine = get_engine(config_name)
    session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))
    return session

def init_db(config_name=None):
    '''
    在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在元数据上。
    否则你就必须在调用 SQLAlchemy() 之前导入它们。
    '''
    print(config_name)

    engine = get_engine(config_name)
    from app import models
    session = create_scoped_session(engine)
    Base.query = session.query_property()
    Base.metadata.create_all(bind=engine)



def db_drop(config_name=None):
    """
    在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在元数据上。
    否则你就必须在调用 SQLAlchemy() 之前导入它们。
    """
    engine = get_engine(config_name)
    from app import models
    Base.metadata.drop_all(bind=engine)
