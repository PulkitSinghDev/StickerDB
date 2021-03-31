import logging
import sqlite3


class StickersDB:
    """
    An object that abstracts the database for storing the sticker data
    It uses sqlite3 as its database engine.
    """

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')
        self.db_path = 'stickers.db'

    def create_table(self):
        """
        Create new table in the database, call this method only when
        the bot encounters a table not found exception
        """
        try:
            query = """CREATE TABLE Stickers (StickerID INTEGER PRIMARY KEY
            AUTOINCREMENT, StickerNAME TEXT, StickerURL TEXT,
            StickerLOC TEXT)"""
            db_conn = sqlite3.connect(self.db_path)
            logging.info(
                '[OK] Database opened successfully for creating new table')
            db_conn.execute(query)
            db_conn.commit()
        except sqlite3.Error as e:
            logging.warning('[FAIL] '+e.args[0])
        finally:
            if db_conn:
                db_conn.close()
                logging.info("""[OK] Database connection closed
                after creating the table""")

    def save_sticker(self, name, url, path):
        """
        Save sticker info to the database, call this method after you've saved
        the sticker image to the disk.
        :param name: Name of the sticker pack
        :param url: Url of the sticker pack
        :param path: Path to locally saved sticker image(preview)
        """
        try:
            query = """INSERT INTO Stickers (StickerName, StickerURL,
            StickerLOC) VALUES(?, ?, ?)"""
            db_conn = sqlite3.connect(self.db_path)
            logging.info(
                '[OK] Database opened successfully for updating new entry')
            db_conn.execute(query, (name, url, path))
            db_conn.commit()
        except sqlite3.Error as e:
            logging.warning('[FAIL] '+e.args[0])
        finally:
            if db_conn:
                db_conn.close()
                logging.info('[OK] Database connection closed')

    def fetch_list(self):
        """
        Fetch the list of entries in the database
        Call this method to populate the bot stickers page
        :return list: a list of ID, Name, URL and Path to Preview
        """
        try:
            query = 'SELECT * FROM Stickers'
            db_conn = sqlite3.connect(self.db_path)
            db_cur = db_conn.cursor()
            logging.info(
                '[OK] Database opened successfully for fetching the list')
            list = []
            for row in db_cur.execute(query):
                list.append(row)
            return list
        except sqlite3.Error as e:
            logging.warning('[FAIL] '+e.args[0])
            return None
        finally:
            if db_conn:
                db_conn.close()
                logging.info('[OK] Database connection closed')
