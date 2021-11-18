import datetime
import sqlite3

class DatabaseHandler:

    def __init__(self, db_path) -> None:
        self._con = sqlite3.connect(f'{db_path}/videos.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    def __del__(self):
        self._con.close()

    def _create_table(self):
        cursor = self._con.cursor()

        cursor.execute('CREATE TABLE videos (creation_date text, detection_id text);')
        self._con.commit()

    def _execute(self, query, params):
        cursor = self._con.cursor()
        if len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='videos';").fetchall()) == 0:
            self._create_table()

        return cursor.execute(query, params).fetchall()

    def _execute_insert(self, query, params):
        self._execute(query, params)
        self._con.commit()

    def push_video(self, video_path):
        query = "INSERT INTO videos(creation_date, detection_id) values (datetime('now'), ?);"
        params = (video_path,)
        self._execute_insert(query, params)

    def get_videos(self, max_date=datetime.datetime(2000,1,1)):
        query = "SELECT * FROM videos WHERE date(creation_date) BETWEEN date(?) AND date('now');"
        params = (max_date.strftime('%Y-%m-%d %H:%M:%S'),)
        return self._execute(query, params)


        
