# main_reforestacion.py
import tkinter as tk
from tkinter import ttk, messagebox
from reforest_engine import SPECIES, SOIL_MOD, plan_reforestation

def on_calculate():
    try:
        area = float(area_entry.get())
        distance = float(distance_entry.get())
        surv_pct = float(surv_entry.get()) / 100.0
        species = species_var.get()
        soil = soil_var.get()

        res = plan_reforestation(area_m2=area,
                                 distance_m=distance,
                                 user_survival_frac=surv_pct,
                                 species_name=species,
                                 soil_type=soil)
        # Mostrar resultado
        out.delete('1.0', tk.END)
        out.insert(tk.END, f"Capacidad teórica (árboles): {res['capacidad_teorica']}\n")
        out.insert(tk.END, f"Supervivencia efectiva: {res['supervivencia_efectiva']*100:.2f}% (incluye efecto suelo)\n")
        out.insert(tk.END, f"Árboles a plantar: {res['arboles_a_plantar']}\n")
        out.insert(tk.END, f"Árboles extra (para compensar mortalidad): {res['arboles_extra']}\n")
        out.insert(tk.END, f"Costo unitario ({res['costo_unitario']}): {res['costo_total']}\n")
        out.insert(tk.END, f"Árboles esperados supervivientes: {res['arboles_esperados_supervivientes']}\n")
        out.insert(tk.END, f"CO₂ anual estimado (kg): {res['co2_anual_estimado_kg']}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Planificador de Reforestación")

frame = ttk.Frame(root, padding=12)
frame.grid()

ttk.Label(frame, text="Área disponible (m²):").grid(column=0, row=0, sticky='w')
area_entry = ttk.Entry(frame); area_entry.grid(column=1, row=0)
area_entry.insert(0, "1000")

ttk.Label(frame, text="Distancia mínima entre árboles (m):").grid(column=0, row=1, sticky='w')
distance_entry = ttk.Entry(frame); distance_entry.grid(column=1, row=1)
distance_entry.insert(0, "3")

ttk.Label(frame, text="Supervivencia esperada (%):").grid(column=0, row=2, sticky='w')
surv_entry = ttk.Entry(frame); surv_entry.grid(column=1, row=2)
surv_entry.insert(0, "80")

ttk.Label(frame, text="Tipo de suelo:").grid(column=0, row=3, sticky='w')
soil_var = tk.StringVar(value=list(SOIL_MOD.keys())[0])
soil_menu = ttk.OptionMenu(frame, soil_var, soil_var.get(), *SOIL_MOD.keys())
soil_menu.grid(column=1, row=3)

ttk.Label(frame, text="Especie:").grid(column=0, row=4, sticky='w')
species_var = tk.StringVar(value=list(SPECIES.keys())[0])
species_menu = ttk.OptionMenu(frame, species_var, species_var.get(), *SPECIES.keys())
species_menu.grid(column=1, row=4)

calc_btn = ttk.Button(frame, text="Calcular plan", command=on_calculate)
calc_btn.grid(column=0, row=5, columnspan=2, pady=8)

out = tk.Text(frame, width=60, height=10)
out.grid(column=0, row=6, columnspan=2)

root.mainloop()
