# reforest_engine.py
from typing import Tuple, Dict
import math

# Datos por defecto (puedes editar o ampliar)
SPECIES: Dict[str, Dict[str, float]] = {
    "Pino":     {"cost": 45.0, "co2": 12.0},   # costo por árbol (moneda) y captura CO2 anual (kg)
    "Encino":   {"cost": 80.0, "co2": 18.0},
    "Acacia":   {"cost": 30.0, "co2": 8.0},
    "Mango":    {"cost": 65.0, "co2": 15.0}
}

SOIL_MOD: Dict[str, float] = {
    "franco/loam": 1.00,
    "arenoso": 0.90,
    "arcilloso": 0.95,
    "rocoso": 0.80
}

def capacity_from_area(area_m2: float, distance_m: float) -> int:
    """
    Calcula capacidad máxima de árboles en área según distancia mínima (malla cuadrada).
    """
    if area_m2 <= 0 or distance_m <= 0:
        return 0
    cap = math.floor(area_m2 / (distance_m ** 2))
    return max(0, cap)

def effective_survival(user_survival_frac: float, soil_type: str) -> float:
    """
    Aplica el modificador de suelo a la tasa de supervivencia dada por el usuario.
    user_survival_frac: debe ser entre 0 y 1 (ej. 0.8 para 80%).
    """
    mod = SOIL_MOD.get(soil_type, 1.0)
    eff = user_survival_frac * mod
    # acotar entre 0.0 y 1.0
    return min(max(eff, 0.0), 1.0)

def plan_reforestation(area_m2: float,
                       distance_m: float,
                       user_survival_frac: float,
                       species_name: str,
                       species_db: Dict[str, Dict[str, float]] = SPECIES,
                       soil_type: str = "franco/loam"
                       ) -> Dict[str, float]:
    """
    Retorna un diccionario con los resultados:
    - capacidad, supervivencia_efectiva, arboles_a_plantar, arboles_extra,
      costo_total, co2_anual_estimado, arboles_esperados_survivientes
    """
    if area_m2 < 0 or distance_m <= 0:
        raise ValueError("Área debe ser >=0 y distancia > 0.")
    if not (0 <= user_survival_frac <= 1):
        raise ValueError("Supervivencia debe estar entre 0 y 1 (p.ej. 0.8 para 80%).")
    if species_name not in species_db:
        raise KeyError(f"Especie '{species_name}' no está en la base de datos.")

    cap = capacity_from_area(area_m2, distance_m)
    surv_eff = effective_survival(user_survival_frac, soil_type)

    if surv_eff == 0:
        arboles_a_plantar = 0
    else:
        arboles_a_plantar = math.ceil(cap / surv_eff)

    arboles_extra = max(0, arboles_a_plantar - cap)
    costo_unit = species_db[species_name]["cost"]
    co2_unit = species_db[species_name]["co2"]

    # estimaciones
    arboles_esperados_survivientes = arboles_a_plantar * surv_eff  # valor real esperado
    # pero el 'objetivo' de capacidad es cap; mostramos ambos
    costo_total = arboles_a_plantar * costo_unit
    co2_anual_total = arboles_esperados_survivientes * co2_unit

    return {
        "capacidad_teorica": cap,
        "supervivencia_efectiva": round(surv_eff, 4),
        "arboles_a_plantar": arboles_a_plantar,
        "arboles_extra": arboles_extra,
        "costo_total": round(costo_total, 2),
        "co2_anual_estimado_kg": round(co2_anual_total, 2),
        "arboles_esperados_supervivientes": round(arboles_esperados_survivientes, 2),
        "costo_unitario": costo_unit,
        "co2_unitario_kg": co2_unit,
        "soil_modifier": SOIL_MOD.get(soil_type, 1.0)
    }
