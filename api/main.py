from typing import Union
import uvicorn
from fastapi import FastAPI
from services.db.connect_to_db import connect

app = FastAPI()

connection = connect()

@app.get("/")
def read_root():
    if connection:
        # Create a cursor object using the connection
        cursor = connection.cursor()

        # Example query: Select all from a table
        cursor.execute("SELECT * FROM company")

        # Fetch all rows from the query
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return rows


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    """
    Run the FastAPI application with Uvicorn server.
    
    This allows you to run the application directly with:
    $ python main.py
    
    Alternatively, you can still use the Uvicorn command:
    $ uvicorn main:app --reload
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all available network interfaces
        port=8000,       # Port to run the server on
        reload=True,     # Auto-reload when files change
        log_level="info" # Log level
    )