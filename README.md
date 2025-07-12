# Cashflow-Optimization-for-Coppel

```markdown
# 💸 Coppel Liquidity Optimization Hub

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![PuLP](https://img.shields.io/badge/Optimization-PuLP-success)](https://coin-or.github.io/pulp/)
[![Status](https://img.shields.io/badge/Status-Final-green)]()

> Daily cash redistribution optimization for 21 Coppel branches using MILP, real data, and geospatial visualization.

---

## 🧠 Project Overview

This project implements a **Mixed-Integer Linear Programming (MILP)** model to optimize cash redistribution across **21 Coppel branches** in Guadalajara. It uses real sales, deposits, and geographic data to minimize:

- Physical transportation costs ($/km)
- Electronic transfer fees (0.1%)
- Insurance over transported cash (0.3%)
- Cash collection costs (0.5%)

The model is built in Python using **PuLP**, and it is executed daily. It includes a **web interface** ("Coppel Logistics Intelligence Hub") with AI-powered insights using Gemini API.

---

## 🖥️ Interface Preview

<p align="center">
  <img src="docs/interface_screenshot.png" width="600" alt="Coppel Logistics Hub Web Interface"/>
</p>

---

## 📁 Project Structure

```
.
├── model.py                 # MILP model code
├── data/
│   ├── Monday.csv ...       # Daily sales/deposits data
│   └── dist_matrix_final.csv
├── docs/
│   └── interface_screenshot.png
├── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your_user/coppel-liquidity-hub.git
cd coppel-liquidity-hub
pip install pulp pandas numpy
```

---

## 🚀 Running the Model

```bash
python model.py
```

The model will solve one instance per day (7 in total) and display:

- Daily optimized cost
- Physical and electronic transfers
- Active variables (routes, amounts, trips)

---

## 📊 Key Results

| Day      | Total Cost (MXN) | Trips | Cash Moved (MXN) | Electronic Transfers |
|----------|------------------|-------|-------------------|----------------------|
| Monday   | $34,663          | 4     | $160,584          | $2,033,361           |
| Thursday | **$29,295**      | 6     | $259,557          | $1,331,803           |
| Saturday | **$40,761**      | 4     | $87,936           | $3,182,362           |
| Average  | $32,422          | 5.6   | $212,847          | $1,748,717           |

---

## 📈 Sensitivity Analysis

- +10% logistics cost → +8% total cost
- -50% vehicle capacity → +12% more trips
- Model remains feasible under moderate parameter shifts

---

## 🔍 Model Summary

### Variables

- `x_ij`: Cash sent from branch i to branch j
- `y_i`: Cash electronically deposited from branch i
- `t_ij`: Number of vehicle trips between branches i and j

### Objective Function

```math
min Z = Σ(25·d_ij·t_ij + 0.003·x_ij) + 0.001·Σ y_i + 0.005·Σ total cash collected
```

### Constraints

- Cash in branch ∈ [$150k, $250k]
- Vehicle capacity = $100,000
- Minimum deposit = 30% of cash sales
- No self-transfers: x_ii = 0

---

## 🧾 Main Code (`model.py`)

<details>
<summary>Click to expand code</summary>

```python
import pulp
import pandas as pd

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

for day in days:
    data = pd.read_csv(f"data/{day}.csv")
    distance_df = pd.read_csv("data/dist_matrix_final.csv")
    distance_df.drop(columns=["Tienda"], inplace=True)

    d = [[distance_df.iloc[i, j] for j in range(21)] for i in range(21)]
    sales = data["promedio_venta"].tolist()
    deposits = data["promedio_abonos"].tolist()
    cash_generated = data["total_promedio"].tolist()

    x_names = [f"x_{i}_{j}" for i in range(21) for j in range(21)]
    t_names = [f"t_{i}_{j}" for i in range(21) for j in range(21)]
    y_names = [f"y_{i}" for i in range(21)]

    x = pulp.LpVariable.dicts("Cash_Moved", x_names, lowBound=0, cat="Continuous")
    t = pulp.LpVariable.dicts("Trip_Count", t_names, lowBound=0, cat="Integer")
    y = pulp.LpVariable.dicts("Electronic_Transfer", y_names, lowBound=0, cat="Continuous")

    model = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

    model += pulp.lpSum(25 * d[i][j] * t[f"t_{i}_{j}"] + 0.003 * x[f"x_{i}_{j}"] for i in range(21) for j in range(21))
    model += 0.001 * pulp.lpSum(y[f"y_{i}"] for i in range(21))
    model += 0.005 * sum(sales[i] + deposits[i] for i in range(21))

    for i in range(21):
        inflow = pulp.lpSum(x[f"x_{j}_{i}"] for j in range(21) if i != j)
        outflow = pulp.lpSum(x[f"x_{i}_{j}"] for j in range(21) if i != j)
        model += (cash_generated[i] + inflow - outflow - y[f"y_{i}"] <= 250000)
        model += (cash_generated[i] + inflow - outflow - y[f"y_{i}"] >= 150000)
        model += (y[f"y_{i}"] >= 0.3 * sales[i])

    for i in range(21):
        for j in range(21):
            if i == j:
                model += (x[f"x_{i}_{j}"] == 0)
                model += (t[f"t_{i}_{j}"] == 0)
            else:
                model += (x[f"x_{i}_{j}"] <= 100000 * t[f"t_{i}_{j}"])

    model.solve()
    print(f"\nResults for {day} - Status: {pulp.LpStatus[model.status]}")
    if model.objective:
        print("Total cost:", pulp.value(model.objective))
        for v in model.variables():
            if v.varValue and v.varValue > 0:
                print(f"{v.name} = {v.varValue}")
```

</details>

---

## 👥 Authors

This project was developed by students from **Tecnológico de Monterrey, Campus Guadalajara**:

- Santiago Pérez Mendoza  
- Yoseba Michel Mireles Ahumada  
- Andrés Martínez Almazán  
- **Josué Tapia Hernández**  
- José Emilio Martínez Hernández  
- Diego Arechiga Bonilla  

---
## 📄 License

This project is currently not licensed for public reuse.
Contact the authors if you wish to use or adapt the model.


---

## 💬 Contact

Interested in replicating this solution in your organization?  
Feel free to reach out via GitHub or LinkedIn 🚀
```
