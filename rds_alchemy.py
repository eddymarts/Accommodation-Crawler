from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import DateTime, Float
from sqlalchemy.pool import QueuePool

class DB_factory:
    def __init__(self, sqlite_filepath="property_db.sqlite3") -> None:

        self.engine = create_engine(
            f"postgresql://scott:tiger@accommodation-202107.cjp3g463xyzn.eu-west-2.rds.amazonaws.com:5432/",
            echo=False,
            pool_size=20,
            poolclass=QueuePool,
        )
        # self.engine = create_engine(f"sqlite:///{sqlite_filepath}", echo=True)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)