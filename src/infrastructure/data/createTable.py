from sqlalchemy import create_engine
from dotenv import load_dotenv
from src.infrastructure.models.models import Base
import os



def create_tables(DATABASE_URL: str):
    load_dotenv()  # Carga las variables de entorno desde el archivo .env
    engine = create_engine(DATABASE_URL, future=True)
    Base.metadata.create_all(bind=engine)
    

    # Verifica si la URL de la base de datos está configurada
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL no está configurada en las variables de entorno.")


if __name__ == "__main__":  
    DATABASE_URL="postgresql://SeusTech_adm:p6niS9FM4ATdM8POq0nx@db-seustech-1.cd2824u62rji.us-east-2.rds.amazonaws.com:5432/DB_Bot_Pedidos"
    create_tables(DATABASE_URL) 
    DB_URL = os.getenv(DATABASE_URL)
    print("Tablas creadas exitosamente.")