#api_model.py
import requests
from database.database import Database
from tabulate import tabulate

class ApiModel:
    def __init__(self):
        self.db = Database()
        self.api_url = "https://www.datos.gov.co/resource/gkvy-gxyv.json"
        self.per_page = 10  

    def fetch_and_store_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            
            self.db.execute_query("TRUNCATE TABLE api_convocatorias")
            
            for item in data:
                query = """
                INSERT INTO api_convocatorias 
                (no_convocatoria, año, nombre_convocatoria, nombre_ganador, area, modalidad, nombre_proyecto)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    int(item.get('no', 0)),
                    item.get('a_o', ''), 
                    item.get('convocatoria', ''),
                    item.get('nombre_ganador', ''),
                    item.get('area', ''),
                    item.get('modalidad', ''),
                    item.get('nombre_proyecto', '')
                )
                self.db.execute_query(query, params)
            
            return True, f"Datos actualizados correctamente. Total registros: {len(data)}"
        except Exception as e:
            return False, f"Error al obtener datos de la API: {str(e)}"

    def get_all_data_paginated(self, page=1):
        """Obtiene datos por pagina de la tabla api_convocatorias"""
        offset = (page - 1) * self.per_page
        query = f"SELECT * FROM api_convocatorias LIMIT {self.per_page} OFFSET {offset}"
        data = self.db.execute_query(query)
        total_query = "SELECT COUNT(*) as total FROM api_convocatorias"
        total = self.db.execute_query(total_query)[0]['total']
        
        return {
            'data': data,
            'current_page': page,
            'per_page': self.per_page,
            'total': total,
            'total_pages': (total + self.per_page - 1) // self.per_page
        }

    def get_data_by_area(self, area):
        """Obtiene datos filtrados por área"""
        query = "SELECT * FROM api_convocatorias WHERE area = %s"
        return self.db.execute_query(query, (area,))

    def get_data_by_modalidad(self, modalidad):
        """Obtiene datos filtrados por modalidad"""
        query = "SELECT * FROM api_convocatorias WHERE modalidad = %s"
        return self.db.execute_query(query, (modalidad,))

    def get_areas_stats(self):
        """Obtiene estadísticas por área"""
        query = """
        SELECT area, COUNT(*) as cantidad 
        FROM api_convocatorias 
        GROUP BY area 
        ORDER BY cantidad DESC
        """
        return self.db.execute_query(query)

    def get_modalidades_stats(self):
        """Obtiene estadísticas por modalidad"""
        query = """
        SELECT modalidad, COUNT(*) as cantidad 
        FROM api_convocatorias 
        GROUP BY modalidad 
        ORDER BY cantidad DESC
        """
        return self.db.execute_query(query)

    def display_data(self, data, title=""):
        """Muestra datos en formato de tabla"""
        if not data:
            print("No hay datos para mostrar")
            return
        
        headers = data[0].keys()
        rows = [item.values() for item in data]
        print(f"\n{title}")
        print(tabulate(rows, headers=headers, tablefmt="grid"))