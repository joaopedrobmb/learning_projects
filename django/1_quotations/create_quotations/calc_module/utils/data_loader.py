import sys
import re
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual (src/utils)
project_root = os.path.abspath(os.path.join(base_dir, "../.."))  # Diretório raiz do projeto (PRICING)
geometric_data_excel_file_path = os.path.join(project_root, "data", "geometric_data.xlsx")  # Caminho absoluto para o arquivo Excel
materials_prices_excel_file_path = os.path.join(project_root, "data", "material_cost.xlsx")  # Caminho absoluto para o arquivo Excel
labor_excel_file_path = os.path.join(project_root, "data", "labor_cost.xlsx")
tax_data_excel_file_path = os.path.join(project_root, "data", "tax_data.xlsx")
sys.path.append(project_root)

import math
import numpy as np
import pandas as pd
from config import *

def load_fp_data():
        df_fp = pd.read_excel(geometric_data_excel_file_path, sheet_name='fundo_plano')

        df_fpCleaned = df_fp   
        df_fpCleaned[['superficial_area(m2)','structural_thickness(mm)']] = df_fpCleaned[['superficial_area(m2)', 'structural_thickness(mm)']].astype(float)
        df_fpCleaned[['diameter(mm)']] = df_fpCleaned[['diameter(mm)']].astype(int)
        df_fpCleaned[['superficial_area(m2)','structural_thickness(mm)']] = df_fpCleaned[['superficial_area(m2)','structural_thickness(mm)']].round(2)

        df_fpCleaned['superficial_area(m2)'] = pd.to_numeric(df_fpCleaned['superficial_area(m2)'], errors='coerce')
        df_fpCleaned['structural_thickness(mm)'] = pd.to_numeric(df_fpCleaned['structural_thickness(mm)'], errors='coerce')
        df_fpCleaned['diameter(mm)'] = pd.to_numeric(df_fpCleaned['diameter(mm)'], errors='coerce')

        return df_fpCleaned

def load_te_data():
        df_te = pd.read_excel(geometric_data_excel_file_path, sheet_name='tampo_eliptico')

        df_teCleaned = df_te    
        df_teCleaned[['volume(m3)','superficial_area(m2)','structural_thickness(mm)']] = df_teCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']].astype(float)
        df_teCleaned[['diameter(mm)']] = df_teCleaned[['diameter(mm)']].astype(int)
        df_teCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']] = df_teCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']].round(2)

        df_teCleaned['superficial_area(m2)'] = pd.to_numeric(df_teCleaned['superficial_area(m2)'], errors='coerce')
        df_teCleaned['structural_thickness(mm)'] = pd.to_numeric(df_teCleaned['structural_thickness(mm)'], errors='coerce')
        df_teCleaned['diameter(mm)'] = pd.to_numeric(df_teCleaned['diameter(mm)'], errors='coerce')

        return df_teCleaned

def load_fc30d_data():
        df_fc30d = pd.read_excel(geometric_data_excel_file_path, sheet_name='fundo_conico_30')

        df_fc30dCleaned = df_fc30d     
        df_fc30dCleaned[['volume(m3)','superficial_area(m2)','structural_thickness(mm)']] = df_fc30dCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']].astype(float)
        df_fc30dCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']] = df_fc30dCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']].round(2)

        return df_fc30dCleaned

def load_fc45d_data():
        df_fc30d = pd.read_excel(geometric_data_excel_file_path, sheet_name='fundo_conico_45')

        df_fc45dCleaned = df_fc30d     
        df_fc45dCleaned[['volume(m3)','superficial_area(m2)']] = df_fc45dCleaned[['volume(m3)', 'superficial_area(m2)']].astype(float)
        df_fc45dCleaned[['volume(m3)', 'superficial_area(m2)']] = df_fc45dCleaned[['volume(m3)', 'superficial_area(m2)']].round(2)

        return df_fc45dCleaned

def load_fc60d_data():
        df_fc60d = pd.read_excel(geometric_data_excel_file_path, sheet_name='fundo_conico_60')

        df_fc60dCleaned = df_fc60d     
        df_fc60dCleaned[['volume(m3)','superficial_area(m2)','structural_thickness(mm)']] = df_fc60dCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']].astype(float)
        df_fc60dCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']] = df_fc60dCleaned[['volume(m3)', 'superficial_area(m2)','structural_thickness(mm)']].round(2)

        return df_fc60dCleaned

def load_flanges_data():
        df_flanges = pd.read_excel(geometric_data_excel_file_path, sheet_name='flanges')

        df_flangesCleaned = df_flanges     
        df_flangesCleaned= df_flangesCleaned.astype(float)
        df_flangesCleaned = df_flangesCleaned.round(2)

        return df_flangesCleaned

def load_manholes_data():
        df_manholes = pd.read_excel(geometric_data_excel_file_path, sheet_name='manholes')

        return df_manholes

def load_inspection_holes_data():
        df_inspection_hole = pd.read_excel(geometric_data_excel_file_path, sheet_name='inspection_holes')

        return df_inspection_hole

def load_safety_railings_ac_data():
        df_safety_railings = pd.read_excel(geometric_data_excel_file_path, sheet_name='safety_railings_AC')

        return df_safety_railings

def load_safety_railings_prfv_data():
        df_safety_railings = pd.read_excel(geometric_data_excel_file_path, sheet_name='safety_railings_PRFV')

        return df_safety_railings

def load_ladder_ac_data():
        df_ladder = pd.read_excel(geometric_data_excel_file_path, sheet_name='ladder_AC')

        return df_ladder

def load_ladder_prfv_data():
        df_ladder = pd.read_excel(geometric_data_excel_file_path, sheet_name='ladder_PRFV')

        return df_ladder

def load_platform_data():
        df_platform = pd.read_excel(geometric_data_excel_file_path, sheet_name='plataforma')

        return {
                row["element"]: {"profile": row["profile"], "needed": row["needed"]}
                for _, row in df_platform.iterrows()
        }

def load_vent_data():
        df_vent = pd.read_excel(geometric_data_excel_file_path, sheet_name='vent')

        return df_vent

def load_prices(df_costs):
    """Carrega os preços a partir do dataframe."""
    return dict(zip(df_costs["Item"], df_costs["Preço"]))

def load_profile_prices_data():
        df_profile_prices = pd.read_excel(materials_prices_excel_file_path, sheet_name='Perfis')

        return df_profile_prices

def load_paint_prices_data():
        df_paint_prices = pd.read_excel(materials_prices_excel_file_path, sheet_name='Tintas')

        return df_paint_prices

def load_fasteners_prices_data():
        df_fasteners_prices = pd.read_excel(materials_prices_excel_file_path, sheet_name='Fixadores')

        return df_fasteners_prices

def load_pvc_prices_data():
        df_pvc_prices = pd.read_excel(materials_prices_excel_file_path, sheet_name='PVC')

        return df_pvc_prices

def load_gasket_prices_data():
        df_gasket_prices = pd.read_excel(materials_prices_excel_file_path, sheet_name='Vedações')

        return df_gasket_prices

def load_resin_prices_data():
        df_resin_prices_data = pd.read_excel(materials_prices_excel_file_path, sheet_name='Resina')

        return df_resin_prices_data

def load_fiber_prices_data():
        df_fiber_prices_data = pd.read_excel(materials_prices_excel_file_path, sheet_name='Fibra')

        return df_fiber_prices_data

def load_chemical_products_prices_data():
        df_quimical_products_data = pd.read_excel(materials_prices_excel_file_path, sheet_name='Produtos Diversos')

        return df_quimical_products_data

def load_tax_data():
        df_tax_data = pd.read_excel(tax_data_excel_file_path, sheet_name='Impostos')

        return df_tax_data

def load_tax_rates(df_tax_rates):
    """Carrega os valores de impostos a partir do DataFrame."""
    return {
        row["Estado"]: {"ICMS": row["ICMS"], "DIFAL": row["DIFAL"]}
        for _, row in df_tax_rates.iterrows()
    }
    
def load_materials_dict(df_fasteners_price):
    materials_dict = {}
    
    for _, row in df_fasteners_price.iterrows():
        item = row["Item"]
        material = row["Material"]
        preco = row["Preço"]

        if item not in materials_dict:
            materials_dict[item] = {}  # Cria um dicionário para esse item

        materials_dict[item][material] = preco  # Associa o material ao preço

    return materials_dict

def load_labor_cost():
        df_labor_cost = pd.read_excel(labor_excel_file_path, sheet_name='Funcionários')

        return df_labor_cost

def load_tank_labor_time():
        df_tank_labor_time = pd.read_excel(labor_excel_file_path, sheet_name='FPTE')

        return df_tank_labor_time

def load_ladder_labor_time():
        df_ladder_labor_time = pd.read_excel(labor_excel_file_path, sheet_name='Escada')

        return df_ladder_labor_time

def load_safety_railings_labor_time():
        df_safety_railings_labor_time = pd.read_excel(labor_excel_file_path, sheet_name='Guarda-Corpo')

        return df_safety_railings_labor_time