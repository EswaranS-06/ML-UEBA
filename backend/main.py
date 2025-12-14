import uvicorn
from storage.init_db import init_db

if __name__ == "__main__":
    init_db()
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
