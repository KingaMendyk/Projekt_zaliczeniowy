import sqlite3


class DbSQL:

    def __init__(self, databasename, filename):
        self.databasename = databasename
        self.create()
        self.read_from_file(filename)

    def create(self):
        try:
            conn = sqlite3.connect(self.databasename)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Wines (
                                               alcohol REAL,
                                               malic_acid REAL,
                                               ash REAL,
                                               alcalinity_of_ash REAL,
                                               magnesium REAL,
                                               total_phenols REAL,
                                               flavanoids REAL,
                                               nonflavanoid_phenols REAL,
                                               proanthocyanins REAL,
                                               color_intensity REAL,
                                               hue REAL,
                                               diluted REAL,
                                               proline REAL,
                                               category TEXT)
                                               ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def fetch_data(self):
        try:
            conn = sqlite3.connect(self.databasename)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Wines")
            res = cursor.fetchall()
            return res
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def read_from_file(self, file):
        conn = sqlite3.connect(self.databasename)
        cursor = conn.cursor()
        cursor.execute("SELECT Count(*) FROM Wines")
        count = cursor.fetchall()[0][0]
        
        if count <= 0:
            with open(file) as file_object:
                for line in file_object:
                    data = line.strip()
                    data = data.split(",")
                    for i in range(len(data)-1):
                        x = data[i]
                        data[i] = float(data[i+1])
                        data[i+1] = x
                    params = tuple(data)
                    sql = "INSERT INTO Wines VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    cursor.execute(sql, params)
                    conn.commit()
        cursor.close()
        conn.close()

    def insert_data(self, data):
        conn = sqlite3.connect(self.databasename)
        cursor = conn.cursor()

        params = tuple(data)
        sql = "INSERT INTO Wines VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()
        conn.close()

    def fetch_names(self):
        conn = sqlite3.connect(self.databasename)
        cursor = conn.execute("SELECT * FROM Wines")
        names = [description[0] for description in cursor.description]
        cursor.close()
        conn.close()
        return names
