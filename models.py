from sqlalchemy import create_engine, Column, Integer, Float, String, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class TrackPoint(Base):
    __tablename__ = 'a_prl' # Mapping to the migrated table for now
    
    # We need a primary key. SQLite adds a hidden rowid, but SQLAlchemy needs an explicit PK.
    # Since the DBF didn't have one, we might need to use the rowid or a composite key.
    # For now, let's assume STN (Station) is unique enough or just use a synthetic ID if we migrated one.
    # Actually, pandas to_sql doesn't add a PK by default.
    # We'll map to the existing columns.
    
    # Since we don't have a clear PK, we'll use a trick or just read-only for now.
    # Or we can add a rowid column in the model if we use the specific sqlite dialect.
    
    # Let's try to map the columns we saw.
    # TNO (FLOAT), LT (TEXT), STN (FLOAT), ERL (FLOAT), PRL (FLOAT)
    
    # We'll use STN as PK for the model definition, but be careful.
    # Using synthetic ID as PK
    id = Column(Integer, primary_key=True)
    STN = Column(Float) 
    TNO = Column(Float)
    LT = Column(String)
    ERL = Column(Float)
    PRL = Column(Float)
    # CUT and FILL are calculated fields, not in DB
    
    def __repr__(self):
        return f"<TrackPoint(STN={self.STN}, ERL={self.ERL}, PRL={self.PRL})>"

def get_engine(db_path):
    return create_engine(f'sqlite:///{db_path}')

def get_session(db_path):
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
