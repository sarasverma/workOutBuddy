import sqlite3, os
class Database():
    def __init__(self, database, table):
        self.database = database
        self.table = table
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.create_table()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.commit()
        self.connection.close()

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS {}(
                    id TEXT PRIMARY KEY NOT NULL, title TEXT NOT NULL,
                    channel TEXT NOT NULL, view_count INTEGER NOT NULL,
                    channel_id TEXT NOT NULL, duration INTEGER NOT NULL,
                    categories JSON, tags JSON, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''.format(self.table)
        self.cursor.execute(query)
        self.commit()

    def insert_record(self, data):
        query = '''INSERT INTO {}({}) values ({})'''.format(self.table, ','.join(data.keys()), ','.join(data.values()))
        self.cursor.execute(query)

    def get_all_records(self):
        query = f"SELECT * FROM {self.table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_record(self, id):
        query = f"DELETE FROM {self.table} WHERE id = '{ id }'"
        os.remove(fr'img/{id}.png') # delete thumbnail
        self.cursor.execute(query)

def connectToDb(database, table):
    connection = Database(database, table)
    return connection

if __name__ == "__main__":
    db = Database("workoutBuddy.db", "workouts")
    # db.insert_record(yt.getInfo("https://www.youtube.com/watch?v=K-CrEi0ymMg"))
    # db.delete_record("xFsf-2VZMSk")
    print(db.get_all_records())
    db.close()
