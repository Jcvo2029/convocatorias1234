#convocatoria_model.py
from database.database import Database
from tabulate import tabulate
from datetime import datetime

class ConvocatoriaModel:
    def __init__(self):
        self.db = Database()

    def crear_convocatoria(self, nombre, fecha_inicio, fecha_fin, cupos, nombre_proyecto, area, modalidad):
        """Crea una nueva convocatoria"""
        query = """
        INSERT INTO convocatorias 
        (nombre, fecha_inicio, fecha_fin, cupos, nombre_proyecto, area, modalidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (nombre, fecha_inicio, fecha_fin, cupos, nombre_proyecto, area, modalidad)
        return self.db.execute_query(query, params)

    def obtener_convocatorias(self, estado=None):
        """Obtiene todas las convocatorias, opcionalmente filtradas por estado"""
        if estado:
            query = "SELECT * FROM convocatorias WHERE estado = %s ORDER BY fecha_inicio DESC"
            return self.db.execute_query(query, (estado,))
        else:
            query = "SELECT * FROM convocatorias ORDER BY fecha_inicio DESC"
            return self.db.execute_query(query)

    def obtener_convocatoria_por_id(self, id):
        """Obtiene una convocatoria por su ID"""
        query = "SELECT * FROM convocatorias WHERE id = %s"
        result = self.db.execute_query(query, (id,))
        return result[0] if result else None

    def actualizar_convocatoria(self, id, **kwargs):
        """Actualiza los datos de una convocatoria"""
        if not kwargs:
            return False
            
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE convocatorias SET {set_clause} WHERE id = %s"
        params = list(kwargs.values()) + [id]
        return self.db.execute_query(query, params)

    def eliminar_convocatoria(self, id):
        """Elimina una convocatoria"""
        query = "DELETE FROM convocatorias WHERE id = %s"
        return self.db.execute_query(query, (id,))

    def cambiar_estado_convocatoria(self, id, estado):
        """Cambia el estado de una convocatoria (abierta/cerrada)"""
        query = "UPDATE convocatorias SET estado = %s WHERE id = %s"
        return self.db.execute_query(query, (estado, id))

    def verificar_cupos_disponibles(self, id_convocatoria):
        """Verifica si hay cupos disponibles en una convocatoria"""
        query = """
        SELECT c.cupos, COUNT(p.id) as inscritos 
        FROM convocatorias c 
        LEFT JOIN participantes p ON c.id = p.id_convocatoria 
        WHERE c.id = %s 
        GROUP BY c.id
        """
        result = self.db.execute_query(query, (id_convocatoria,))
        if result:
            cupos = result[0]['cupos']
            inscritos = result[0]['inscritos']
            return cupos - inscritos > 0
        return False

    def obtener_convocatorias_abiertas(self):
        """Obtiene convocatorias abiertas con cupos disponibles"""
        query = """
        SELECT c.* 
        FROM convocatorias c
        LEFT JOIN (
            SELECT id_convocatoria, COUNT(*) as total 
            FROM participantes 
            GROUP BY id_convocatoria
        ) p ON c.id = p.id_convocatoria
        WHERE c.estado = 'abierta' 
        AND (p.total IS NULL OR c.cupos > p.total)
        """
        return self.db.execute_query(query)

    def display_convocatorias(self, convocatorias, title=""):
        """Muestra las convocatorias en formato de tabla"""
        if not convocatorias:
            print("No hay convocatorias para mostrar")
            return
        
        headers = convocatorias[0].keys()
        rows = [item.values() for item in convocatorias]
        print(f"\n{title}")
        print(tabulate(rows, headers=headers, tablefmt="grid"))