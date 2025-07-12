
import pulp
import pandas as pd
import numpy as np
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

for day in days:
    data=pd.read_csv(f"{day}.csv")
    distance_df=pd.read_csv("dist_matrix.csv")


    d = []  # lista de distancias

    for i in range(21):  
        row = []
        for j in range(21):
            valor = distance_df.iloc[i, j] 
            row.append(valor)
        d.append(row)


    VentasEF=[]
    Abonos=[]
    Efectivo_generado=[]


    for i in range(21):
        v=data.loc[i,"promedio_venta"]
        VentasEF.append(v)
        v=data.loc[i,"promedio_abonos"]
        Abonos.append(v)
        v=data.loc[i,"total_promedio"]
        Efectivo_generado.append(v)
        

        

            


    x=[] # x[i][j]
    t=[] #t[i][j]
    y=[]    #y[i]
    C_viaje=1e+5
    L=300000
    E_min=200000

    #Definir variables
    for i in range(21):
        for j in range(21):
            str=f"x_{i}_{j}"
            x.append(str)
            str=f"t_{i}_{j}"
            t.append(str)
            str=f"y_{i}"
        y.append(str)


    x_variables=pulp.LpVariable.dicts("Dinero",x,lowBound=0,cat="Continous")
    t_variables=pulp.LpVariable.dicts("Cantidad de viajes",t,lowBound=0,cat="Integer")
    y_variables=pulp.LpVariable.dicts("Transferencias Electrónicas",y,lowBound=0,cat="Continous")

    # 1. Crear el problema de minimización
    modelo = pulp.LpProblem("Minimizar_costo", pulp.LpMinimize)

    
    # Definir la función objetivo (a minimizar)
    modelo+=pulp.lpSum( 25*d[i][j]*t_variables[f"t_{i}_{j}"] +.003*x_variables[f"x_{i}_{j}"] for i in range(21) for j in range(21) )+pulp.lpSum( .001*y_variables[var] for var in y)+.005*pulp.lpSum(VentasEF[i]+Abonos[i] for i in range(21)),"Función Objetivo"

    # Agregar restricciones
    for i in range(21):
        modelo +=(Efectivo_generado[i] +pulp.lpSum(x_variables[f"x_{j}_{i}"] for j in range(21))-pulp.lpSum(x_variables[f"x_{i}_{j}"] for j in range(21))-y_variables[f"y_{i}"] <=L ), f"Restriccion_1_{i}"

    for i in range(21):
        for j in range(21):
            modelo+=(x_variables[f"x_{i}_{j}"]<=C_viaje*t_variables[f"t_{i}_{j}"]),f"Restriccion_2_{i}_{j}"

    for i in range(21):
        modelo +=(Efectivo_generado[i] +pulp.lpSum(x_variables[f"x_{j}_{i}"] for j in range(21))-pulp.lpSum(x_variables[f"x_{i}_{j}"] for j in range(21)) -y_variables[f"y_{i}"] >=E_min ), f"Restriccion_3_{i}"

    for i in range(21):
        modelo+=(y_variables[f"y_{i}"]>=0.3*VentasEF[i]),f"Restriccion 4_{i}"


        
    modelo.solve()
    print(f"Resultados para el dia {day}:")
    print(pulp.LpStatus[modelo.status])
    print("Los costos son: ",pulp.value(modelo.objective))

    for v in modelo.variables():
        if v.varValue>0:
            print(f"{v.name} = {v.varValue}")
