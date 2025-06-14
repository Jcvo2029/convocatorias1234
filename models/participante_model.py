#participante_model.py
from database.database import Database
from tabulate import tabulate
from datetime import datetime

class ParticipanteModel:
    def __init__(self):
        self.db = Database()

    def crear_participante(self, cedula, nombre, apellido, edad, id_convocatoria, fecha_inscripcion=None):
        """Registra un nuevo participante en una convocatoria"""
        try:
            # Verificar si la convocatoria existe y está abierta
            convocatoria = self._obtener_convocatoria(id_convocatoria)
            if not convocatoria or convocatoria['estado'] != 'abierta':
                return False, "La convocatoria no está abierta"
                
            # Verificar cupos disponibles
            inscritos = self.contar_inscritos_convocatoria(id_convocatoria)
            if inscritos >= convocatoria['cupos']:
                return False, "No hay cupos disponibles en esta convocatoria"
                
            # Verificar que no esté ya registrado
            if self.verificar_inscripcion(cedula, id_convocatoria):
                return False, "El participante ya está registrado en esta convocatoria"
            
            if not fecha_inscripcion:
                fecha_inscripcion = datetime.now().date()
            
            query = """
            INSERT INTO participantes 
            (cedula, nombre, apellido, edad, id_convocatoria, fecha_inscripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (cedula, nombre, apellido, edad, id_convocatoria, fecha_inscripcion)
            
            if self.db.execute_query(query, params):
                return True, "Participante registrado exitosamente"
            return False, "Error al registrar participante"
            
        except Exception as e:
            return False, f"Error en la base de datos: {str(e)}"

    def _obtener_convocatoria(self, id_convocatoria):
        """Obtiene los datos de una convocatoria"""
        query = "SELECT id, nombre, estado, cupos FROM convocatorias WHERE id = %s"
        result = self.db.execute_query(query, (id_convocatoria,))
        return result[0] if result else None

    # ... (resto de métodos se mantienen igual)

    def obtener_participantes(self, id_convocatoria=None):
        """Obtiene todos los participantes, opcionalmente filtrados por convocatoria"""
        if id_convocatoria:
            query = """
            SELECT p.*, c.nombre as nombre_convocatoria 
            FROM participantes p
            JOIN convocatorias c ON p.id_convocatoria = c.id
            WHERE p.id_convocatoria = %s
            """
            return self.db.execute_query(query, (id_convocatoria,))
        else:
            query = """
            SELECT p.*, c.nombre as nombre_convocatoria 
            FROM participantes p
            JOIN convocatorias c ON p.id_convocatoria = c.id
            """
            return self.db.execute_query(query)

    def obtener_participante_por_cedula(self, cedula):
        """Obtiene un participante por su cédula"""
        query = """
        SELECT p.*, c.nombre as nombre_convocatoria 
        FROM participantes p
        JOIN convocatorias c ON p.id_convocatoria = c.id
        WHERE p.cedula = %s
        """
        result = self.db.execute_query(query, (cedula,))
        return result[0] if result else None

    def obtener_participante_por_id(self, id):
        """Obtiene un participante por su ID"""
        query = """
        SELECT p.*, c.nombre as nombre_convocatoria 
        FROM participantes p
        JOIN convocatorias c ON p.id_convocatoria = c.id
        WHERE p.id = %s
        """
        result = self.db.execute_query(query, (id,))
        return result[0] if result else None

    def actualizar_participante(self, id, **kwargs):
        """Actualiza los datos de un participante"""
        if not kwargs:
            return False
            
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE participantes SET {set_clause} WHERE id = %s"
        params = list(kwargs.values()) + [id]
        return self.db.execute_query(query, params)

    def eliminar_participante(self, id):
        """Elimina un participante"""
        query = "DELETE FROM participantes WHERE id = %s"
        return self.db.execute_query(query, (id,))

    def verificar_inscripcion(self, cedula, id_convocatoria):
        """Verifica si un participante ya está inscrito en una convocatoria"""
        query = """
        SELECT COUNT(*) as count 
        FROM participantes 
        WHERE cedula = %s AND id_convocatoria = %s
        """
        result = self.db.execute_query(query, (cedula, id_convocatoria))
        return result[0]['count'] > 0 if result else False

    def contar_inscritos_convocatoria(self, id_convocatoria):
        """Cuenta los participantes inscritos en una convocatoria"""
        query = """
        SELECT COUNT(*) as total 
        FROM participantes 
        WHERE id_convocatoria = %s
        """
        result = self.db.execute_query(query, (id_convocatoria,))
        return result[0]['total'] if result else 0

    def display_participantes(self, participantes, title=""):
        """Muestra los participantes en formato de tabla"""
        if not participantes:
            print("No hay participantes para mostrar")
            return
        
        headers = participantes[0].keys()
        rows = [item.values() for item in participantes]
        print(f"\n{title}")
        print(tabulate(rows, headers=headers, tablefmt="grid"))