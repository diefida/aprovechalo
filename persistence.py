import configparser
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class Configuration:
    def __init__(self, configuration_path):
        self.config_path = configuration_path
        self._configuration = self._get_configuration_from_path()

    def _open_ini_file(self):
        configuration_file = open(self.config_path)
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_file(configuration_file)
        configuration_file.close()

        return config

    def _get_configuration_from_path(self):
        config = self._open_ini_file()
        configuration = {}

        for section in config.sections():
            configuration[section] = {}
            for option in config.options(section):
                value = config.get(section, option)
                if option == 'port':
                    value = int(value)
                configuration[section][option] = value
        return configuration

    @property
    def persistence(self):
        persistence_config = self._configuration['database']
        if persistence_config['driver'] == 'sqlite':
            engine_str = 'sqlite:///' + persistence_config['file']
        elif persistence_config['driver'] in ('mysql', 'postgresql'):
            engine_str = persistence_config['driver'] + '://' + \
                         persistence_config['user'] + ":" + \
                         persistence_config['password'] + \
                         '@' + persistence_config['host'] + \
                         ':' + persistence_config['port'] + \
                         '/' + persistence_config['database_name']
        else:
            raise Exception('')

        return engine_str

    @property
    def server(self):
        return self._configuration['server']


class _Base(object):
    """Base class for SQLAlchemy model classes."""
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}


Base = declarative_base(cls=_Base)


class DatabaseManager:
    def __init__(self, engine_url):
        self._configuration = engine_url
        if engine_url.split(":")[0] == "sqlite":
            self._engine = create_engine(engine_url,
                                         connect_args={
                                             'check_same_thread': False
                                         })
        else:
            self._engine = create_engine(engine_url,
                                         pool_size=20,
                                         max_overflow=0)

        session_factory = sessionmaker(bind=self._engine,
                                       expire_on_commit=False,
                                       autoflush=False,
                                       autocommit=False)

        def uniq_session():
            return 'value'

        self._Session = scoped_session(session_factory, scopefunc=uniq_session)

    @property
    def configuration(self):
        return self._configuration

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self._Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise

    def create_schema(self):
        Base.metadata.create_all(self._engine, checkfirst=True)

    def drop_schema(self):
        Base.metadata.drop_all(self._engine)
