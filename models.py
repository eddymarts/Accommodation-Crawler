from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import DateTime, Float


Base = declarative_base()

class UrlToScrape(Base):
    __tablename__ = 'urls_to_scrape'

    id = Column(Integer, primary_key=True)
    url = Column(String,index=True)
    parser_to_use = Column(String) # Category - so we can scrape multiple sites easily -- can just parse the URL when it's fetched
    scraped_yet = Column(String, default=False, nullable=False)
    # date_modified = Column(String, nullable=False)

    def __repr__(self):
       return self.url



class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    country = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String)
    post_code = Column(String) # important one
    long_lat = Column(String)

    # area - Square-footage = Column(String)
    area_m_2 = Column(Float)
    number_of_bedrooms = Column(Integer)
    number_of_bathrooms = Column(Integer)

    is_rental = Column(Boolean)
    is_shared_accomodation = Column(Boolean)
    is_student = Column(Boolean)
    is_furnished = Column(Boolean)

    price_per_month_gbp = Column(Float, index=True)
    property_type = Column(String) # Flat/house/detached/semi-detached
    
    url = Column(String)
    description = Column(String)
    pictures = Column(String)

    updated_date = Column(DateTime)

    def __repr__(self):
       return f"property: {self.name}"


class DB_factory():
    def __init__(self, sqlite_filepath="property_db.sqlite3") -> None:
        
        self.engine = create_engine(f"sqlite:///{sqlite_filepath}", echo=False)

        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session()