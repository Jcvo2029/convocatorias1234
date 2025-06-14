#api_controller.py
from models.api_model import ApiModel

class ApiController:
    def __init__(self):
        self.model = ApiModel()

    def update_api_data(self):
        success, message = self.model.fetch_and_store_data()
        print(message)
        return success

    def show_all_data_paginated(self, page=1):
        data = self.model.get_all_data_paginated(page)
        self.model.display_data(data['data'], f"Convocatorias API - Página {page} de {data['total_pages']}")
        return data

    def show_data_by_area(self, area):
        data = self.model.get_data_by_area(area)
        self.model.display_data(data, f"Convocatorias API - Área: {area}")

    def show_data_by_modalidad(self, modalidad):
        data = self.model.get_data_by_modalidad(modalidad)
        self.model.display_data(data, f"Convocatorias API - Modalidad: {modalidad}")

    def show_areas_stats(self):
        data = self.model.get_areas_stats()
        self.model.display_data(data, "Estadísticas por Área")

    def show_modalidades_stats(self):
        data = self.model.get_modalidades_stats()
        self.model.display_data(data, "Estadísticas por Modalidad")