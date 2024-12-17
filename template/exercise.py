from fastapi import FastAPI
import sqlite3


# TODO replace these sample queries with the ones you need to load the sample data
def load_data(db):
    db.execute("PRAGMA foreign_keys = ON;")
    db.execute("CREATE TABLE some_table(some_column TEXT);")
    db.executemany("INSERT INTO some_table VALUES(:foo);", [{"foo": "abc"}, {"foo": "def"}])
    db.commit()


# For simplicity, this template uses a global, temporary, in-memory database
db = sqlite3.connect(":memory:")
load_data(db)


app = FastAPI()

# TODO replace this sample endpoint with the ones requested in the exercise
@app.get("/test")
async def test_endpoint():
    return {"test_query_response": db.execute("SELECT * FROM some_table;").fetchall()}
