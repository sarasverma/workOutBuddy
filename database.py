import sqlite3, os
class Database():
    def __init__(self, database, table):
        self.database = database
        self.table = table

        # getting a schema
        if table == 'workouts':
            self.schema = '''id TEXT PRIMARY KEY NOT NULL, title TEXT NOT NULL,
                    channel TEXT NOT NULL, view_count INTEGER NOT NULL,
                    channel_id TEXT NOT NULL, duration INTEGER NOT NULL,
                    categories JSON, tags JSON, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'''
        elif table == 'calories':
            self.schema = '''date DATESTAMP PRIMARY KEY DEFAULT (date()),
                    calories_burnt INTEGER DEFAULT 0'''
        else:
            raise Exception("Schema not found !")
        
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.create_table()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.commit()
        self.connection.close()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS {}({})'''.format(self.table, self.schema)
        self.cursor.execute(query)
        self.commit()

    def insert_record(self, data):
        query = '''INSERT INTO {}({}) values ({})'''.format(self.table, ','.join(data.keys()), ','.join(data.values()))
        self.cursor.execute(query)
        self.commit()

    def get_all_records(self):
        query = f"SELECT * FROM {self.table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_record(self, field, value):
        query = f"SELECT * FROM {self.table} WHERE {field} = '{value}'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_record(self, field, id, setField, value):
        query = f"UPDATE {self.table} SET {setField} = {value} WHERE {field} = '{id}'"
        self.cursor.execute(query)
        self.commit()

    def delete_record(self, field, value):
        query = f"DELETE FROM {self.table} WHERE {field} = '{ value }'"
        if self.table == 'workouts':
            os.remove(fr'img/{id}.png') # delete thumbnail
        self.cursor.execute(query)
        self.commit()

def connectToDb(database, table):
    connection = Database(database, table)
    return connection

if __name__ == "__main__":
    db = Database("workoutBuddy.db", "workouts")
    # db.insert_record(yt.getInfo("https://www.youtube.com/watch?v=K-CrEi0ymMg"))
    # db.delete_record("xFsf-2VZMSk")
    print(db.get_all_records())
    db.close()
