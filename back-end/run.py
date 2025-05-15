from dotenv import load_dotenv
load_dotenv()  # Carrega as variáveis do arquivo .env

from app.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
