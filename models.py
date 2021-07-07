from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import DateTime, Float
from sqlalchemy.pool import QueuePool


Base = declarative_base()


class UrlToScrape(Base):
    __tablename__ = "urls_to_scrape"

    id = Column(Integer, primary_key=True)
    url = Column(String, index=True)
    parser_to_use = Column(
        String
    )  # Category - so we can scrape multiple sites easily -- can just parse the URL when it's fetched
    scraped_yet = Column(String, default=False, nullable=False)

    def __repr__(self):
        return f"{self.id}-{self.url}"


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    country = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String)
    post_code = Column(String)  # important one
    longitude = Column(Float)
    latitude = Column(Float)

    # area - Square-footage = Column(String)
    area_m_2 = Column(Float)
    number_of_bedrooms = Column(Integer)
    number_of_bathrooms = Column(Integer)

    is_rental = Column(Boolean)
    is_shared_accomodation = Column(Boolean)
    is_student = Column(Boolean)
    is_furnished = Column(Boolean)

    price_for_sale = Column(Float, index=True)
    price_per_month_gbp = Column(Float, index=True)

    property_type = Column(String)  # Flat/house/detached/semi-detached

    url = Column(String)
    description = Column(String)
    agency = Column(String)
    agency_phone_number = Column(String)
    google_maps = Column(String)
    pictures = Column(String)

    updated_date = Column(DateTime)

    def __repr__(self):
        return f"""Property: 
        id -- {self.id}
        country -- {self.country}
        city -- {self.city}
        address -- {self.address}
        post_code -- {self.post_code}
        longitude -- {self.longitude}
        latitude -- {self.latitude}

        area_m_2 -- {self.area_m_2}
        number_of_bedrooms -- {self.number_of_bedrooms}
        number_of_bathrooms -- {self.number_of_bathrooms}
        is_furnished -- {self.is_furnished}
        price_per_month_gbp -- {self.price_per_month_gbp}
        price_for_sale -- {self.price_for_sale}
        property_type -- {self.property_type}
        url -- {self.url}

        pictures -- {self.pictures}
        updated_date -- {self.updated_date}
       """


class DB_factory:
    def __init__(self, sqlite_filepath="property_db.sqlite3") -> None:

        self.engine = create_engine(
            f"sqlite:///{sqlite_filepath}",
            echo=False,
            pool_size=20,
            poolclass=QueuePool,
        )
        # self.engine = create_engine(f"sqlite:///{sqlite_filepath}", echo=True)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session()

    # need to call engine.dispose() before using in a multithreaded process
    # More details on sql_alchemy and multiProcessing:
    # https://docs.sqlalchemy.org/en/14/core/pooling.html#using-connection-pools-with-multiprocessing
    def get_fresh_session_for_multiprocessing(self):
        self.engine.dispose()
        new_session = sessionmaker(bind=self.engine)
        return new_session()
