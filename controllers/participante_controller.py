#participante_controller.py
from models.participante_model import ParticipanteModel
from datetime import datetime

class ParticipanteController:
    def __init__(self):
        self.model = ParticipanteModel()

    def registrar_participante(self, data):
        try:
            if data['edad'] < 18:
                return False, "El participante debe tener al menos 18 años"
            
            return self.model.crear_participante(
                data['cedula'],
                data['nombre'],
                data['apellido'],
                data['edad'],
                data['id_convocatoria'],
                data.get('fecha_inscripcion')
            )
            
        except Exception as e:
            return False, f"Error al registrar participante: {str(e)}"


    def _validar_convocatoria(self, id_convocatoria):
        query = "SELECT estado, fecha_inicio FROM convocatorias WHERE id = %s"
        result = self.model.db.execute_query(query, (id_convocatoria,))
        if not result or result[0]['estado'] != 'abierta':
            return False
        
        return self.model.verificar_cupos_disponibles(id_convocatoria)

    def listar_participantes(self, id_convocatoria=None):
        return self.model.obtener_participantes(id_convocatoria)

    def obtener_participante(self, identificador, por_cedula=True):
        if por_cedula:
            return self.model.obtener_participante_por_cedula(identificador)
        else:
            return self.model.obtener_participante_por_id(identificador)

    def actualizar_participante(self, id, data):
        participante = self.model.obtener_participante_por_id(id)
        if not participante:
            return False, "Participante no encontrado"
        
        if self.model.actualizar_participante(id, **data):
            return True, "Participante actualizado exitosamente"
        return False, "Error al actualizar participante"

    def eliminar_participante(self, id):
        if self.model.eliminar_participante(id):
            return True, "Participante eliminado exitosamente"
        return False, "Error al eliminar participante"

    def contar_inscritos(self, id_convocatoria):
        return self.model.contar_inscritos_convocatoria(id_convocatoria)

    def mostrar_participantes(self, participantes, title=""):
        self.model.display_participantes(participantes, title)