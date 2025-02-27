import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import *

def calculate_hydrostatic_pressure (height, fluid_density): # Calcula a pressão hidrostática em função da altura e densidade do fluido;
    hydrostatic_pressure = height*(fluid_density*KGCM3_TO_KGMM3)
    return hydrostatic_pressure

def calculate_volume_tank(diameter, cylindrical_length):
    tank_volume = np.pi*((diameter)/2)**2*cylindrical_length*MM3_TO_M3 # Calcula o volume do tanque em m^3;

    return tank_volume

def calculate_thickness_shell(diameter,cylindrical_length):
    F = 10 # Design factor ASME RTP-1;
    fluid_density = 1.0 # Densidade da água em kg/cm^3;

    pressure = calculate_hydrostatic_pressure(cylindrical_length, fluid_density) # Calcula a pressão hidrostática em função da altura e densidade do fluido;
    shell_thickness = (pressure*diameter)/(2*((S_FW*MPA_TO_KGFMM2)/F)) # Calculo a espessura do costado em mm;

    return round(shell_thickness,2)

def calculate_mass_cylindrical_body(diameter, length, thickness,material_density):

    cylindrical_body_mass = np.pi*diameter*length*thickness*material_density/1000000000 # Calcula a massa do corpo cilíndrico em kg;

    return cylindrical_body_mass

def calculate_mass_elliptical_body(diameter, thickness, material_density, df_te):
    def get_area_elliptical_head(diameter, df_te):
        if not isinstance(df_te, pd.DataFrame):
            raise ValueError("df_te precisa ser um DataFrame!")

        row = df_te[df_te['diameter(mm)'] == diameter]

        if row.empty:
            raise ValueError(f'Diametro {diameter} não encontrado na base de dados.')

        return row['superficial_area(m2)'].values[0]

    superficial_area = get_area_elliptical_head(diameter,df_te)
    elliptical_head_mass = superficial_area*(thickness*MM_TO_M)*material_density

    return elliptical_head_mass

def calculate_mass_flat_bottom(diameter, thickness, material_density, df_fp):
    def get_area_flat_bottom(diameter, df_fp):

        row = df_fp[df_fp['diameter(mm)']==diameter]

        if row.empty:
            raise ValueError(f'Diametro {diameter} não encontrado na base de dados.')

        return row['superficial_area(m2)'].values[0]

    superficial_area = get_area_flat_bottom(diameter, df_fp)

    flat_bottom_mass = superficial_area*(thickness*MM_TO_M)*material_density

    return flat_bottom_mass

def calculate_mass_circunferencial_joints(diameter, thickness):

    circunferencial_joint_width = 300

    return round((np.pi*diameter*circunferencial_joint_width*thickness)*D_HLU*MM3_TO_M3)

def calculate_mass_longitudinal_joints(cylindrical_length, thickness):

    longitudinal_joint_width = 300

    return round(cylindrical_length*longitudinal_joint_width*thickness*D_HLU*MM3_TO_M3)

def calculate_flange_mass(flange_diameter,neck_thickness, neck_length, face_diameter, face_thickness, material_density):
    def calculate_flange_neck_mass(flange_diameter, neck_thickness, neck_length, material_density):
        return (flange_diameter*IN_TO_MM)*np.pi*neck_length*neck_thickness*material_density*MM3_TO_M3

    def calculate_flange_face_mass(face_diameter, flange_diameter, face_thickness, material_density):
        return ((((face_diameter*IN_TO_MM)/2)**2*np.pi)-(((flange_diameter*IN_TO_MM)/2)**2*np.pi))*face_thickness*material_density*MM3_TO_M3

    return calculate_flange_neck_mass(flange_diameter, neck_thickness, neck_length, material_density)+calculate_flange_face_mass(face_diameter, flange_diameter, face_thickness, material_density)

def calculate_blind_flange_mass(face_diameter, blind_flange_thickness, material_density):
    return (face_diameter*IN_TO_MM/2)**2*np.pi*blind_flange_thickness*material_density*MM3_TO_M3

def calculate_flange_lamination_mass(lamination_diameter, flange_diameter, circunferencial_lamination_thickness, neck_lamination_thickness,neck_lamination_length):
    def calculate_circunferencial_lamination_mass(lamination_diameter, flange_diameter, circunferencial_lamination_thickness):
        return (((lamination_diameter/2)**2*np.pi)-((flange_diameter*IN_TO_MM/2)**2*np.pi))*circunferencial_lamination_thickness*D_HLU*MM3_TO_M3

    def calculate_neck_lamination_mass(flange_diameter, neck_lamination_length, neck_lamination_thickness):
        return flange_diameter*IN_TO_MM*np.pi*neck_lamination_length*neck_lamination_thickness*D_HLU*MM3_TO_M3

    return calculate_circunferencial_lamination_mass(lamination_diameter, flange_diameter, circunferencial_lamination_thickness)+calculate_neck_lamination_mass(flange_diameter, neck_lamination_length, neck_lamination_thickness)

def calculate_total_superficial_area(diameter, cylindrical_length, df_bottom, df_head):
    def get_area_elliptical_head(diameter, df_te):
        if not isinstance(df_te, pd.DataFrame):
            raise ValueError("df_te precisa ser um DataFrame!")

        row = df_te[df_te['diameter(mm)'] == diameter]

        if row.empty:
            raise ValueError(f'Diametro {diameter} não encontrado na base de dados.')

        return row['superficial_area(m2)'].values[0]

    def get_area_flat_bottom(diameter, df_fp):

        row = df_fp[df_fp['diameter(mm)']==diameter]

        if row.empty:
            raise ValueError(f'Diametro {diameter} não encontrado na base de dados.')

        return row['superficial_area(m2)'].values[0]

    total_superficial_area = get_area_flat_bottom(diameter, df_bottom) + get_area_elliptical_head(diameter, df_head) + (diameter*np.pi*cylindrical_length*MM2_TO_M2)

    return total_superficial_area

def calculate_paint_consumption(superficial_area):

    return superficial_area/PAINT_RATE

def calculate_laminate_cost(lamination_type, resin_type, dict_resin_costs, dict_fiber_costs):
    """Calcula o custo do laminado com base no tipo de laminação e resina."""
    fiber_map = {
        "SU": ("R2400", RESIN_SU, FIBER_SU),
        "HLU1": ("M450", RESIN_HLU1, FIBER_HLU1),
        "HLU2": (["M450", "T800"], RESIN_HLU2, FIBER_HLU2),
        "FW": ("R2200", RESIN_FW, FIBER_FW),
        "VEIL": ("Véu", RESIN_VEIL, FIBER_VEIL)        
    }

    if lamination_type not in fiber_map:
        raise ValueError(f"Tipo de laminação inválido: {lamination_type}")

    fibers, resin_proportion, fiber_proportion = fiber_map[lamination_type]

    if isinstance(fibers, list):  # Caso especial HLU2 (2 fibras)
        fiber1_cost = MANTA_HLU2 * dict_fiber_costs.get(fibers[0], 0)
        fiber2_cost = TECIDO_HLU2 * dict_fiber_costs.get(fibers[1], 0)
        total_fiber_cost = fiber1_cost + fiber2_cost
    else:
        total_fiber_cost = fiber_proportion * dict_fiber_costs.get(fibers, 0)

    laminate_cost = (resin_proportion * dict_resin_costs.get(resin_type, 0)) + total_fiber_cost
    return round(laminate_cost, 2)

def get_resin_proportion(lamination_type):
    """Retorna a proporção de resina para cada tipo de laminação."""
    resin_proportions = {
        "SU": RESIN_SU,
        "HLU1": RESIN_HLU1,
        "HLU2": RESIN_HLU2,
        "FW": RESIN_FW
    }
    return resin_proportions.get(lamination_type, 0)  # Retorna 0 caso o tipo não seja encontrado
    
def calculate_chemical_products_cost(lamination_type, resin_type, catalysis_type, dict_chemical_products_costs):
    """Calcula o custo dos produtos químicos no processo de laminação, considerando a proporção correta de resina."""
    
    # Criamos um mapeamento estático dos catalisadores básicos para cada tipo de catálise
    catalyst_map = {
        "MECKP/COBALTO": ["MECKP", "Thinner", "Estireno"],
        "BPO/DMA": ["BPO", "DMA", "Thinner", "Estireno"]
    }

    if catalysis_type not in catalyst_map:
        raise ValueError(f"Tipo de catálise inválido: {catalysis_type}")

    # Obtém a proporção de resina com base no tipo de laminação
    resin_proportion = get_resin_proportion(lamination_type)

    # Criamos uma cópia da lista de catalisadores para evitar modificar o dicionário global
    catalyst_list = catalyst_map[catalysis_type][:]

    # Se for MECKP/COBALTO com resinas especiais, adicionamos Cobalto e DMA
    if catalysis_type == "MECKP/COBALTO" and resin_type in ["Estervinílica", "Derakane 411", "Derakane 470"]:
        catalyst_list.extend(["Cobalto 6%", "DMA"])  

    # Mapeia as proporções dos produtos químicos
    proportions = {
        "MECKP": MECKP_PROPORTION, "Thinner": THINNER_PROPORTION, "Estireno": STYRENE_PROPORTION,
        "BPO": BPO_PROPORTION, "DMA": DMA_PROPORTION, "Cobalto 6%": COBALT_PROPORTION
    }

    # Calcula o custo individual de cada produto químico na lista correta
    chemical_products_cost = sum(proportions.get(item, 0) * dict_chemical_products_costs.get(item, 0) for item in catalyst_list)

    # Multiplica pelo fator correto de proporção da resina
    total_chemical_cost = resin_proportion * chemical_products_cost

    return round(total_chemical_cost, 2)

def calculate_laminate_total_cost(lamination_type, resin_type, catalysis_type, dict_resin_costs, dict_fiber_costs, dict_chemical_products_costs):
    """Calcula o custo total do laminado incluindo resina, fibra e produtos químicos."""

    laminate_cost = calculate_laminate_cost(lamination_type, resin_type, dict_resin_costs, dict_fiber_costs)
    chemical_cost = calculate_chemical_products_cost(lamination_type, resin_type, catalysis_type, dict_chemical_products_costs)

    return laminate_cost + chemical_cost