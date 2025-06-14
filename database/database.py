import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance
    
    def _initialize_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            print("Conexión a la base de datos establecida correctamente")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            raise
    
    def execute_query(self, query, params=None):
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                return result if result else None
                
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos cerrada")
    
    def __del__(self):
        self.close()