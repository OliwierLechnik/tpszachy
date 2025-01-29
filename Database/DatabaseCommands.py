import sqlite3

class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect("Games.db")
        self.cursor = self.conn.cursor()
        self.createDB()

    def createDB(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS moves (
                GameID INTEGER NOT NULL,
                MoveID INTEGER NOT NULL,
                Move TEXT NOT NULL,
                PRIMARY KEY (GameID, MoveID)
            )
        ''')

    def addMoveDB(self,gameID, Move):
        self.cursor.execute("SELECT COALESCE(MAX(MoveID), 0) + 1 FROM moves WHERE GameID = ?", (gameID,))
        next_move_id = self.cursor.fetchone()[0]  # Fetch the next MoveID

        self.cursor.execute("INSERT INTO moves (GameID, MoveID, Move) VALUES (?, ?, ?)",
                       (gameID, next_move_id, Move))
        self.conn.commit()

    def getGameFromDB(self,gameID):
        # returns a table of all the moves in the right order
        self.cursor.execute("SELECT Move FROM moves WHERE GameID = ?", (gameID,))

    def CloseDB(self):
        self.conn.close()
