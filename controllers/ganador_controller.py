from models.ganador_model import GanadorModel
from models.participante_model import ParticipanteModel
from models.convocatoria_model import ConvocatoriaModel

class GanadorController:
    def __init__(self):
        self.model = GanadorModel()
        self.participante_model = ParticipanteModel()
        self.convocatoria_model = ConvocatoriaModel()

    def registrar_ganador(self, id_participante, id_convocatoria):
        try:
            convocatoria = self.convocatoria_model.obtener_convocatoria_por_id(id_convocatoria)
            if not convocatoria:
                return False, "Convocatoria no encontrada"
            if convocatoria['estado'] != 'cerrada':
                return False, "La convocatoria debe estar cerrada para asignar ganadores"
            
            return self.model.crear_ganador(id_participante, id_convocatoria)
            
        except Exception as e:
            return False, f"Error al registrar ganador: {str(e)}"

    def listar_ganadores(self, id_convocatoria=None):
        return self.model.obtener_ganadores(id_convocatoria)

        return self.model.obtener_ganador_por_id(id)

    def eliminar_ganador(self, id):
        try:
            if self.model.eliminar_ganador(id):
                return True, "Ganador eliminado exitosamente"
            return False, "Error al eliminar ganador"
        except Exception as e:
            return False, f"Error al eliminar ganador: {str(e)}"

    def mostrar_ganadores(self, ganadores, title=""):
        self.model.display_ganadores(ganadores, title)

    def generar_reporte_ganadores(self):
        try:
            query = """
            SELECT c.id, c.nombre, COUNT(g.id) as total_ganadores
            FROM convocatorias c
            LEFT JOIN ganadores g ON c.id = g.id_convocatoria
            WHERE c.estado = 'cerrada'
            GROUP BY c.id
            ORDER BY c.fecha_inicio DESC
            """
            convocatorias = self.model.db.execute_query(query)
            
            if not convocatorias:
                return False, "No hay convocatorias cerradas con ganadores registrados"
            
            reporte = []
            for conv in convocatorias:
                ganadores = self.listar_ganadores(conv['id'])
                reporte.append({
                    'convocatoria': conv['nombre'],
                    'total_ganadores': conv['total_ganadores'],
                    'ganadores': ganadores
                })
            
            return True, reporte
            
        except Exception as e:
            return False, f"Error al generar reporte: {str(e)}"