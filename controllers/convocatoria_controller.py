#convocatoraia_model.py
from models.convocatoria_model import ConvocatoriaModel
from datetime import datetime

class ConvocatoriaController:
    def __init__(self):
        self.model = ConvocatoriaModel()

    def crear_convocatoria(self, data):
        """Valida y crea una nueva convocatoria"""
        try:
            fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date()
            
            if fecha_fin <= fecha_inicio:
                return False, "La fecha de fin debe ser posterior a la fecha de inicio"
            
            if self.model.crear_convocatoria(
                data['nombre'],
                data['fecha_inicio'],
                data['fecha_fin'],
                data['cupos'],
                data.get('nombre_proyecto', ''),
                data['area'],
                data['modalidad']
            ):
                return True, "Convocatoria creada exitosamente"
            return False, "Error al crear la convocatoria"
        except ValueError as e:
            return False, f"Formato de fecha incorrecto: {str(e)}"
        except Exception as e:
            return False, f"Error al crear convocatoria: {str(e)}"

    def listar_convocatorias(self, estado=None):
        return self.model.obtener_convocatorias(estado)

    def obtener_convocatoria(self, id):
        return self.model.obtener_convocatoria_por_id(id)

    def actualizar_convocatoria(self, id, data):
        convocatoria = self.model.obtener_convocatoria_por_id(id)
        if not convocatoria:
            return False, "Convocatoria no encontrada"
        
        if 'fecha_inicio' in data or 'fecha_fin' in data:
            fecha_inicio = datetime.strptime(data.get('fecha_inicio', convocatoria['fecha_inicio']), '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(data.get('fecha_fin', convocatoria['fecha_fin']), '%Y-%m-%d').date()
            
            if fecha_fin <= fecha_inicio:
                return False, "La fecha de fin debe ser posterior a la fecha de inicio"
        
        if self.model.actualizar_convocatoria(id, **data):
            return True, "Convocatoria actualizada exitosamente"
        return False, "Error al actualizar la convocatoria"

    def eliminar_convocatoria(self, id):
        if self.model.eliminar_convocatoria(id):
            return True, "Convocatoria eliminada exitosamente"
        return False, "Error al eliminar la convocatoria"

    def cambiar_estado_convocatoria(self, id, estado):
        if estado not in ['abierta', 'cerrada']:
            return False, "Estado no válido"
        
        if self.model.cambiar_estado_convocatoria(id, estado):
            return True, f"Estado de convocatoria cambiado a '{estado}'"
        return False, "Error al cambiar el estado de la convocatoria"

    def verificar_cupos(self, id_convocatoria):
        return self.model.verificar_cupos_disponibles(id_convocatoria)

    def listar_convocatorias_abiertas(self):
        return self.model.obtener_convocatorias_abiertas()

    def mostrar_convocatorias(self, convocatorias, title=""):
        self.model.display_convocatorias(convocatorias, title)
        