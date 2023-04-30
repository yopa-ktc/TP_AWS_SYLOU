import csv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Repository_leaderboard import LeaderBoard_Repository

engine = create_engine("sqlite:///leaderboard.db", pool_pre_ping=True)
# create the table
declarative_base().metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# open the CSV file
with open("pipeline_result.csv", newline='') as csvfile:
    # create a CSV reader object
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # iterate over each row in the file
    next(reader, None)
    for row in reader:
        # create a new leaderboard entry
        add_leaderboard = LeaderBoard_Repository(session)
        add_leaderboard.create_Leaderboard(row[0], "yopa", row[1])

session.close()
    
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import data from a CSV file into a database.')
    parser.add_argument('db_uri', help='URI of the database')
    parser.add_argument('csv_path', help='Path to the CSV file')
    args = parser.parse_args()

    main(args.db_uri, args.csv_path)
"""
