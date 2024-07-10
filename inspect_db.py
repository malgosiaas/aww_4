from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Define the database URL
DATABASE_URL = "sqlite:///./test.db"

# Create an engine and metadata object
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect the tables
metadata.reflect(bind=engine)

# List all tables
print("Tables:")
for table in metadata.tables:
    print(table)

# Describe the 'images' table if it exists
if 'images' in metadata.tables:
    images_table = metadata.tables['images']
    print("\nSchema for 'images' table:")
    for column in images_table.columns:
        print(column)

# Describe the 'rectangles' table if it exists
if 'rectangles' in metadata.tables:
    rectangles_table = metadata.tables['rectangles']
    print("\nSchema for 'rectangles' table:")
    for column in rectangles_table.columns:
        print(column)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Query all data from the 'images' table
if 'images' in metadata.tables:
    print("\nData from 'images' table:")
    images = session.query(images_table).all()
    for image in images:
        print(dict(image))

# Query all data from the 'rectangles' table
if 'rectangles' in metadata.tables:
    print("\nData from 'rectangles' table:")
    rectangles = session.query(rectangles_table).all()
    for rectangle in rectangles:
        print(dict(rectangle))

# Close the session
session.close()
