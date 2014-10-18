# db_create.py

from project import db

# creates the database and the table
db.create_all()

# test data to insert
#db.session.add(Task("Finish this tutorial", date(2014, 3, 13), 10, 1))
#db.session.add(Task("Finish Real Python", date(2014, 3, 13), 10, 1))

# as usual commit your data
db.session.commit()