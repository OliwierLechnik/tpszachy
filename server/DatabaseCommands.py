import sqlite3

class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect("Games.db")
        self.cursor = self.conn.cursor()
        self.createDB()

    def createDB(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS moves (
                GameID TEXT NOT NULL,
                MoveID INTEGER NOT NULL,
                Move TEXT NOT NULL,
                PRIMARY KEY (GameID, MoveID)
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS GameInfo (
            GameID TEXT PRIMARY KEY,
            PlayerCount INTEGER
        )
        ''')

        self.conn.commit()




    def addMoveDB(self,gameID, Move):

        self.cursor.execute("SELECT COALESCE(MAX(MoveID), 0) + 1 FROM moves WHERE GameID = ?", (gameID,))
        next_move_id = self.cursor.fetchone()[0]  # Fetch the next MoveID

        self.cursor.execute("INSERT INTO moves (GameID, MoveID, Move) VALUES (?, ?, ?)",
                       (gameID, next_move_id, Move))
        self.conn.commit()

    def addGameInfoDB(self,gameID, PlayerCount):
        self.cursor.execute("INSERT INTO GameInfo (GameID, PlayerCount) VALUES (?, ?)",
                            (gameID, PlayerCount))


    def getGameFromDB(self,gameID):
        # returns a table of all the moves in the right order
        self.cursor.execute("SELECT Move FROM moves WHERE GameID = ?", (gameID,))
        MoveTouples = DB.cursor.fetchall()

        MoveList = []
        for Move in MoveTouples:
            MoveList.append(Move[0])

        return MoveList

    def getAllGameIDs(self):
        self.cursor.execute("SELECT GameID FROM GameInfo")
        IDTouples = DB.cursor.fetchall()

        IDs = []
        for ID in IDTouples:
            IDs.append(ID[0])
        return IDs

    def CloseDB(self):
        self.conn.close()


DB = DataBase()
Moves = DB.getGameFromDB("25d01681-7b58-4dcc-a41e-10da0eba9c7d")
Games = DB.getAllGameIDs()
print(Games)
