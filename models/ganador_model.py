from database.database import Database
from tabulate import tabulate

class GanadorModel:
    def __init__(self):
        self.db = Database()
        
    def crear_ganador(self, id_participante, id_convocatoria):
        """Registra un nuevo ganador"""
        try:
            # Verificar que el participante existe y pertenece a la convocatoria
            participante = self._obtener_participante(id_participante)
            if not participante or participante['id_convocatoria'] != id_convocatoria:
                return False, "Participante no válido para esta convocatoria"
            
            # Verificar que no sea ya ganador
            if self._verificar_ganador_existente(id_participante, id_convocatoria):
                return False, "El participante ya es ganador de esta convocatoria"
            
            query = """
            INSERT INTO ganadores 
            (id_participante, nombre, apellido, id_convocatoria) 
            VALUES (%s, %s, %s, %s)
            """
            params = (id_participante, participante['nombre'], participante['apellido'], id_convocatoria)
            
            if self.db.execute_query(query, params):
                return True, "Ganador registrado exitosamente"
            return False, "Error al registrar ganador"
            
        except Exception as e:
            return False, f"Error en la base de datos: {str(e)}"
    
    def _obtener_participante(self, id_participante):
        """Obtiene los datos de un participante"""
        query = "SELECT * FROM participantes WHERE id = %s"
        result = self.db.execute_query(query, (id_participante,))
        return result[0] if result else None
    
    def _verificar_ganador_existente(self, id_participante, id_convocatoria):
        """Verifica si un participante ya es ganador de una convocatoria"""
        query = """
        SELECT COUNT(*) as count 
        FROM ganadores 
        WHERE id_participante = %s AND id_convocatoria = %s
        """
        result = self.db.execute_query(query, (id_participante, id_convocatoria))
        return result[0]['count'] > 0 if result else False
    
    def obtener_ganadores(self, id_convocatoria=None):
        """Obtiene todos los ganadores, opcionalmente filtrados por convocatoria"""
        try:
            if id_convocatoria:
                query = """
                SELECT g.*, c.nombre as nombre_convocatoria 
                FROM ganadores g
                JOIN convocatorias c ON g.id_convocatoria = c.id
                WHERE g.id_convocatoria = %s
                """
                result = self.db.execute_query(query, (id_convocatoria,))
            else:
                query = """
                SELECT g.*, c.nombre as nombre_convocatoria 
                FROM ganadores g
                JOIN convocatorias c ON g.id_convocatoria = c.id
                """
                result = self.db.execute_query(query)
                
            return result if result else []
            
        except Exception as e:
            print(f"Error al obtener ganadores: {str(e)}")
            return []
    
    def obtener_ganador_por_id(self, id):
        """Obtiene un ganador por su ID"""
        query = """
        SELECT g.*, c.nombre as nombre_convocatoria 
        FROM ganadores g
        JOIN convocatorias c ON g.id_convocatoria = c.id
        WHERE g.id = %s
        """
        result = self.db.execute_query(query, (id,))
        return result[0] if result else None
    
    def eliminar_ganador(self, id):
        """Elimina un ganador"""
        try:
            query = "DELETE FROM ganadores WHERE id = %s"
            return self.db.execute_query(query, (id,))
        except Exception as e:
            print(f"Error al eliminar ganador: {str(e)}")
            return False
    
    def display_ganadores(self, ganadores, title=""):
        """Muestra los ganadores en formato de tabla"""
        if not ganadores:
            print("No hay ganadores para mostrar")
            return
        
        headers = ganadores[0].keys()
        rows = [item.values() for item in ganadores]
        print(f"\n{title}")
        print(tabulate(rows, headers=headers, tablefmt="grid"))