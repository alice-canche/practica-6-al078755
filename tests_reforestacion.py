# tests_reforestacion.py
from reforest_engine import plan_reforestation

def run_tests():
    # Caso 1: 1000 m2, distancia 3m, supervivencia 80%, pino, suelo franco
    r1 = plan_reforestation(1000, 3, 0.8, "Pino", soil_type="Franco/loam")
    print("Caso 1:", r1)

    # Caso 2: suelo rocoso (peor supervivencia)
    r2 = plan_reforestation(1000, 3, 0.8, "Pino", soil_type="Rocoso")
    print("Caso 2:", r2)

    # Caso 3: área pequeña que no admite árboles
    r3 = plan_reforestation(2, 3, 0.8, "Acacia", soil_type="Arenoso")
    print("Caso 3:", r3)

if __name__ == "__main__":
    run_tests()
