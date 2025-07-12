# ==============================================================================
# SECCIÓN 1: IMPORTACIÓN DE LIBRERÍAS
# ==============================================================================
import pandas as pd
import json
import webbrowser
import os
import random
from collections import deque
import re
import base64
import numpy as np

# Librerías para generación de mapas
try:
    import folium
    from folium.plugins import AntPath
    from folium.features import CustomIcon
    import osmnx as ox
    import networkx as nx
    MAP_LIBS_AVAILABLE = True
except ImportError:
    print("⚠️ Advertencia: Faltan librerías para generar mapas (folium, osmnx). Se omitirá la creación de mapas animados.")
    MAP_LIBS_AVAILABLE = False

# ==============================================================================
# SECCIÓN 2: CONFIGURACIÓN DE RUTAS Y DATOS
# ==============================================================================
BASE_PATH = r"C:\Users\miche\Downloads\COPPEL\COPPEL"

FILE_PATHS = {
    "dist_matrix": os.path.join(BASE_PATH, "dist_matrix_final.csv"),
    "coordinates": os.path.join(BASE_PATH, "CoppelCoor.csv"),
    "dashboard_template": os.path.join(BASE_PATH, "dashboard_template.html"),
    "coppel_logo": os.path.join(BASE_PATH, "coppel.png"),
    "osmnx_graph": os.path.join(BASE_PATH, "guadalajara_drive.graphml"),
    "output_dashboard": os.path.join(BASE_PATH, "Logistica_Coppel_Reto.html"),
    "output_maps_folder": os.path.join(BASE_PATH, "maps_output_final")
}

GOOGLE_MAPS_API_KEY = "AIzaSyDmHwZfn3sz6ZBqwwXLBZE7RdSd7rMxPOs"

USER_PROVIDED_RESULTS = """
[... El texto largo de los resultados va aquí, sin cambios ...]
Resultados para el dia Monday:
Optimal
Los costos son:  34662.61617666666
Cantidad_de_viajes_t_0_7 = 1.0
Cantidad_de_viajes_t_13_14 = 1.0
Cantidad_de_viajes_t_20_9 = 1.0
Cantidad_de_viajes_t_2_11 = 1.0
Dinero_x_0_7 = 88428.404
Dinero_x_13_14 = 55956.575
Dinero_x_20_9 = 4408.18
Dinero_x_2_11 = 11791.297
Transferencias_Electrónicas_y_0 = 338860.38
Transferencias_Electrónicas_y_1 = 262627.84
Transferencias_Electrónicas_y_10 = 6571.659
Transferencias_Electrónicas_y_11 = 3405.837
Transferencias_Electrónicas_y_12 = 13780.12
Transferencias_Electrónicas_y_13 = 154732.25
Transferencias_Electrónicas_y_14 = 28895.718
Transferencias_Electrónicas_y_15 = 214218.47
Transferencias_Electrónicas_y_16 = 13392.756
Transferencias_Electrónicas_y_17 = 141167.74
Transferencias_Electrónicas_y_18 = 122202.43
Transferencias_Electrónicas_y_19 = 7799.085
Transferencias_Electrónicas_y_2 = 325178.75
Transferencias_Electrónicas_y_20 = 10612.713
Transferencias_Electrónicas_y_3 = 22540.554
Transferencias_Electrónicas_y_4 = 111847.49
Transferencias_Electrónicas_y_5 = 145741.68
Transferencias_Electrónicas_y_6 = 10911.357
Transferencias_Electrónicas_y_7 = 8419.077
Transferencias_Electrónicas_y_8 = 3988.656
Transferencias_Electrónicas_y_9 = 1545.03
Resultados para el dia Tuesday:
Optimal
Los costos son:  30684.623353666662
Cantidad_de_viajes_t_0_7 = 1.0
Cantidad_de_viajes_t_13_14 = 1.0
Cantidad_de_viajes_t_17_19 = 1.0
Cantidad_de_viajes_t_18_9 = 1.0
Cantidad_de_viajes_t_2_11 = 1.0
Cantidad_de_viajes_t_3_6 = 1.0
Dinero_x_0_7 = 66459.912
Dinero_x_13_14 = 46409.503
Dinero_x_17_19 = 3160.179
Dinero_x_18_9 = 41903.894
Dinero_x_2_11 = 26401.772
Dinero_x_3_6 = 2559.241
Transferencias_Electrónicas_y_0 = 295955.59
Transferencias_Electrónicas_y_1 = 222199.73
Transferencias_Electrónicas_y_10 = 6417.159
Transferencias_Electrónicas_y_11 = 2489.562
Transferencias_Electrónicas_y_12 = 9617.271
Transferencias_Electrónicas_y_13 = 92691.817
Transferencias_Electrónicas_y_14 = 38004.213
Transferencias_Electrónicas_y_15 = 108801.43
Transferencias_Electrónicas_y_16 = 13431.672
Transferencias_Electrónicas_y_17 = 65864.361
Transferencias_Electrónicas_y_18 = 13133.937
Transferencias_Electrónicas_y_19 = 7175.709
Transferencias_Electrónicas_y_2 = 244138.88
Transferencias_Electrónicas_y_20 = 7356.447
Transferencias_Electrónicas_y_3 = 20869.926
Transferencias_Electrónicas_y_4 = 88530.55
Transferencias_Electrónicas_y_5 = 47581.06
Transferencias_Electrónicas_y_6 = 8556.111
Transferencias_Electrónicas_y_7 = 5656.752
Transferencias_Electrónicas_y_8 = 4743.783
Transferencias_Electrónicas_y_9 = 1585.974
Resultados para el dia Wednesday:
Optimal
Los costos son:  30448.531655000006
Cantidad_de_viajes_t_0_7 = 1.0
Cantidad_de_viajes_t_13_14 = 1.0
Cantidad_de_viajes_t_18_9 = 1.0
Cantidad_de_viajes_t_2_11 = 1.0
Dinero_x_0_7 = 84126.516
Dinero_x_13_14 = 35484.259
Dinero_x_18_9 = 38974.784
Dinero_x_2_11 = 11379.586
Transferencias_Electrónicas_y_0 = 245042.73
Transferencias_Electrónicas_y_1 = 257412.85
Transferencias_Electrónicas_y_10 = 6603.201
Transferencias_Electrónicas_y_11 = 3186.549
Transferencias_Electrónicas_y_12 = 9920.499
Transferencias_Electrónicas_y_13 = 65580.771
Transferencias_Electrónicas_y_14 = 37216.689
Transferencias_Electrónicas_y_15 = 143444.3
Transferencias_Electrónicas_y_16 = 13575.894
Transferencias_Electrónicas_y_17 = 14184.02
Transferencias_Electrónicas_y_18 = 14189.853
Transferencias_Electrónicas_y_19 = 5953.353
Transferencias_Electrónicas_y_2 = 331705.15
Transferencias_Electrónicas_y_20 = 9383.157
Transferencias_Electrónicas_y_3 = 48054.74
Transferencias_Electrónicas_y_4 = 49750.11
Transferencias_Electrónicas_y_5 = 54085.53
Transferencias_Electrónicas_y_6 = 8080.143
Transferencias_Electrónicas_y_7 = 4297.779
Transferencias_Electrónicas_y_8 = 3839.088
Transferencias_Electrónicas_y_9 = 1835.064
Resultados para el dia Thursday:
Optimal
Los costos son:  29294.82569333333
Cantidad_de_viajes_t_0_7 = 1.0
Cantidad_de_viajes_t_13_14 = 1.0
Cantidad_de_viajes_t_17_19 = 1.0
Cantidad_de_viajes_t_20_9 = 1.0
Cantidad_de_viajes_t_2_11 = 1.0
Cantidad_de_viajes_t_3_6 = 1.0
Dinero_x_0_7 = 93878.08
Dinero_x_13_14 = 71306.655
Dinero_x_17_19 = 24186.201
Dinero_x_20_9 = 38414.563
Dinero_x_2_11 = 26187.454
Dinero_x_3_6 = 5585.099
Transferencias_Electrónicas_y_0 = 319210.69
Transferencias_Electrónicas_y_1 = 223401.35
Transferencias_Electrónicas_y_10 = 6236.967
Transferencias_Electrónicas_y_11 = 2563.377
Transferencias_Electrónicas_y_12 = 8148.381
Transferencias_Electrónicas_y_13 = 54851.945
Transferencias_Electrónicas_y_14 = 25233.762
Transferencias_Electrónicas_y_15 = 93796.59
Transferencias_Electrónicas_y_16 = 11440.695
Transferencias_Electrónicas_y_17 = 13628.358
Transferencias_Electrónicas_y_18 = 24832.107
Transferencias_Electrónicas_y_19 = 6014.721
Transferencias_Electrónicas_y_2 = 255157.38
Transferencias_Electrónicas_y_20 = 11094.174
Transferencias_Electrónicas_y_3 = 18840.981
Transferencias_Electrónicas_y_4 = 72127.99
Transferencias_Electrónicas_y_5 = 16292.97
Transferencias_Electrónicas_y_6 = 9678.129
Transferencias_Electrónicas_y_7 = 5613.48
Transferencias_Electrónicas_y_8 = 4647.834
Transferencias_Electrónicas_y_9 = 930.273
Resultados para el dia Friday:
Optimal
Los costos son:  30066.52598733333
Cantidad_de_viajes_t_0_7 = 1.0
Cantidad_de_viajes_t_13_14 = 1.0
Cantidad_de_viajes_t_15_9 = 1.0
Cantidad_de_viajes_t_17_19 = 1.0
Cantidad_de_viajes_t_20_8 = 1.0
Cantidad_de_viajes_t_2_11 = 1.0
Cantidad_de_viajes_t_3_6 = 1.0
Dinero_x_0_7 = 79537.721
Dinero_x_13_14 = 60035.112
Dinero_x_15_9 = 42057.058
Dinero_x_17_19 = 25667.453
Dinero_x_20_8 = 13929.681
Dinero_x_2_11 = 29787.993
Dinero_x_3_6 = 8154.313
Transferencias_Electrónicas_y_0 = 348391.3
Transferencias_Electrónicas_y_1 = 296366.72
Transferencias_Electrónicas_y_10 = 6455.781
Transferencias_Electrónicas_y_11 = 3321.153
Transferencias_Electrónicas_y_12 = 48938.73
Transferencias_Electrónicas_y_13 = 30082.348
Transferencias_Electrónicas_y_14 = 29864.352
Transferencias_Electrónicas_y_15 = 27654.927
Transferencias_Electrónicas_y_16 = 11416.641
Transferencias_Electrónicas_y_17 = 34441.647
Transferencias_Electrónicas_y_18 = 20370.123
Transferencias_Electrónicas_y_19 = 7252.206
Transferencias_Electrónicas_y_2 = 243048.27
Transferencias_Electrónicas_y_20 = 11965.338
Transferencias_Electrónicas_y_3 = 26319.105
Transferencias_Electrónicas_y_4 = 59542.3
Transferencias_Electrónicas_y_5 = 18642.444
Transferencias_Electrónicas_y_6 = 10802.223
Transferencias_Electrónicas_y_7 = 5341.491
Transferencias_Electrónicas_y_8 = 4781.751
Transferencias_Electrónicas_y_9 = 1656.261
Resultados para el dia Saturday:
Optimal
Los costos son:  40761.33931366668
Cantidad_de_viajes_t_0_7 = 1.0
Cantidad_de_viajes_t_13_14 = 1.0
Cantidad_de_viajes_t_20_9 = 1.0
Cantidad_de_viajes_t_2_11 = 1.0
Dinero_x_0_7 = 50962.045
Dinero_x_13_14 = 14733.98
Dinero_x_20_9 = 6317.991
Dinero_x_2_11 = 15922.364
Transferencias_Electrónicas_y_0 = 708868.11
Transferencias_Electrónicas_y_1 = 514245.29
Transferencias_Electrónicas_y_10 = 10682.823
Transferencias_Electrónicas_y_11 = 5076.594
Transferencias_Electrónicas_y_12 = 122994.88
Transferencias_Electrónicas_y_13 = 235853.29
Transferencias_Electrónicas_y_14 = 40927.473
Transferencias_Electrónicas_y_15 = 186776.27
Transferencias_Electrónicas_y_16 = 23589.513
Transferencias_Electrónicas_y_17 = 109474.46
Transferencias_Electrónicas_y_18 = 111629.51
Transferencias_Electrónicas_y_19 = 11697.108
Transferencias_Electrónicas_y_2 = 405808.76
Transferencias_Electrónicas_y_20 = 21063.573
Transferencias_Electrónicas_y_3 = 57154.6
Transferencias_Electrónicas_y_4 = 220753.31
Transferencias_Electrónicas_y_5 = 136152.77
Transferencias_Electrónicas_y_6 = 15313.221
Transferencias_Electrónicas_y_7 = 13959.945
Transferencias_Electrónicas_y_8 = 4762.596
Transferencias_Electrónicas_y_9 = 2293.611
Resultados para el dia Sunday:
Optimal
Los costos son:  31033.665873
Cantidad_de_viajes_t_0_7 = 1.0
Cantidad_de_viajes_t_13_14 = 1.0
Cantidad_de_viajes_t_17_19 = 1.0
Cantidad_de_viajes_t_18_9 = 1.0
Cantidad_de_viajes_t_1_16 = 1.0
Cantidad_de_viajes_t_20_8 = 1.0
Cantidad_de_viajes_t_2_11 = 1.0
Cantidad_de_viajes_t_3_6 = 1.0
Dinero_x_0_7 = 94789.9
Dinero_x_13_14 = 47974.585
Dinero_x_17_19 = 10584.313
Dinero_x_18_9 = 46354.685
Dinero_x_1_16 = 34951.069
Dinero_x_20_8 = 39009.186
Dinero_x_2_11 = 66821.783
Dinero_x_3_6 = 25697.652
Transferencias_Electrónicas_y_0 = 295593.27
Transferencias_Electrónicas_y_1 = 145807.44
Transferencias_Electrónicas_y_10 = 7930.692
Transferencias_Electrónicas_y_11 = 4143.093
Transferencias_Electrónicas_y_12 = 18638.061
Transferencias_Electrónicas_y_13 = 113744.17
Transferencias_Electrónicas_y_14 = 34929.285
Transferencias_Electrónicas_y_15 = 142527.53
Transferencias_Electrónicas_y_16 = 12791.649
Transferencias_Electrónicas_y_17 = 16678.248
Transferencias_Electrónicas_y_18 = 26881.143
Transferencias_Electrónicas_y_19 = 9863.223
Transferencias_Electrónicas_y_2 = 418873.01
Transferencias_Electrónicas_y_20 = 19776.204
Transferencias_Electrónicas_y_3 = 31066.068
Transferencias_Electrónicas_y_4 = 22626.372
Transferencias_Electrónicas_y_5 = 43883.32
Transferencias_Electrónicas_y_6 = 9577.542
Transferencias_Electrónicas_y_7 = 9762.9
Transferencias_Electrónicas_y_8 = 4138.206
Transferencias_Electrónicas_y_9 = 1991.778
"""

# ==============================================================================
# SECCIÓN 3: FUNCIONES DE MAPAS
# (El código de esta sección es idéntico al de la respuesta anterior, no cambia)
# ==============================================================================
PLACE_NAME = "Guadalajara, Jalisco, Mexico"
OSMNX_GRAPH = None

def cargar_o_descargar_grafo_osmnx():
    global OSMNX_GRAPH
    graph_filepath = FILE_PATHS["osmnx_graph"]
    if not MAP_LIBS_AVAILABLE:
        print("-> Motor de mapas OSMnx no disponible (faltan librerías).")
        return
    if OSMNX_GRAPH is not None:
        print("-> Grafo de calles ya está en memoria.")
        return

    try:
        print(f"-> Intentando cargar grafo de calles desde: {graph_filepath}")
        OSMNX_GRAPH = ox.load_graphml(graph_filepath)
        print(f"✅ Éxito: Grafo de calles '{PLACE_NAME}' cargado correctamente.")
    except FileNotFoundError:
        print(f"ℹ️ Archivo de grafo no encontrado. Descargando para '{PLACE_NAME}' (esto puede tardar)...")
        try:
            OSMNX_GRAPH = ox.graph_from_place(PLACE_NAME, network_type="drive", retain_all=True, truncate_by_edge=True)
            ox.save_graphml(OSMNX_GRAPH, filepath=graph_filepath)
            print(f"✅ Éxito: Grafo descargado y guardado en: {graph_filepath}")
        except Exception as e_graph:
            print(f"🚨 ERROR CRÍTICO con OSMnx al descargar/guardar: {e_graph}. Las rutas del mapa serán líneas rectas.")
            OSMNX_GRAPH = None
    except Exception as e_load:
        print(f"🚨 ERROR CRÍTICO al cargar el grafo desde archivo: {e_load}. Las rutas del mapa serán líneas rectas.")
        OSMNX_GRAPH = None

def obtener_coordenadas_ruta_calle(orig_lat, orig_lon, dest_lat, dest_lon):
    global OSMNX_GRAPH
    if OSMNX_GRAPH is None: return None 
    if abs(orig_lat - dest_lat) < 1e-6 and abs(orig_lon - dest_lon) < 1e-6: return [(orig_lat, orig_lon)]
    try:
        orig_node = ox.nearest_nodes(OSMNX_GRAPH, X=orig_lon, Y=orig_lat)
        dest_node = ox.nearest_nodes(OSMNX_GRAPH, X=dest_lon, Y=dest_lat)
        if orig_node == dest_node: return [(OSMNX_GRAPH.nodes[orig_node]['y'], OSMNX_GRAPH.nodes[orig_node]['x'])]
        route_nodes = nx.shortest_path(OSMNX_GRAPH, orig_node, dest_node, weight="length")
        route_coordinates = [(OSMNX_GRAPH.nodes[node_id]['y'], OSMNX_GRAPH.nodes[node_id]['x']) for node_id in route_nodes]
        return route_coordinates if len(route_coordinates) >= 2 else None
    except (nx.NetworkXNoPath, Exception):
        return None

def generate_animated_map(day_name, day_results, tienda_locations, store_names_map_idx, output_folder):
    # (Esta función es para los mapas individuales y no necesita cambios)
    if not MAP_LIBS_AVAILABLE: return
    print(f"  Generando mapa animado para {day_name}...")
    coppel_logo_path = FILE_PATHS["coppel_logo"]
    coppel_logo_data_uri = None
    try:
        with open(coppel_logo_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        coppel_logo_data_uri = f"data:image/png;base64,{encoded_string}"
    except Exception: pass
    coords = list(tienda_locations.values())
    center_lat = np.mean([c['lat'] for c in coords]) if coords else 20.6736
    center_lon = np.mean([c['lng'] for c in coords]) if coords else -103.344
    mapa_diario = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB positron")
    for idx, store_name in store_names_map_idx.items():
        if store_name not in tienda_locations: continue
        coords = tienda_locations[store_name]
        e_transfer = day_results['raw_y'].get(str(idx), 0.0)
        popup_html = f"<b>{store_name}</b><br>Índice: {idx}<br>"
        if e_transfer > 0: popup_html += f"Transf. Electrónica Enviada: ${e_transfer:,.2f}"
        icon = CustomIcon(icon_image=coppel_logo_data_uri, icon_size=(35,35)) if coppel_logo_data_uri else folium.Icon(color='blue', icon='bank', prefix='fa')
        folium.Marker(location=[coords['lat'], coords['lng']], popup=folium.Popup(popup_html, max_width=300), tooltip=store_name, icon=icon).add_to(mapa_diario)
    for route in day_results.get('routes', []):
        try:
            loc_origen_coords = tienda_locations.get(route['from'])
            loc_destino_coords = tienda_locations.get(route['to'])
            if not loc_origen_coords or not loc_destino_coords: continue
            loc_origen = (loc_origen_coords['lat'], loc_origen_coords['lng'])
            loc_destino = (loc_destino_coords['lat'], loc_destino_coords['lng'])
            ruta_por_calles = obtener_coordenadas_ruta_calle(loc_origen[0], loc_origen[1], loc_destino[0], loc_destino[1])
            ruta_para_mostrar = ruta_por_calles or [loc_origen, loc_destino]
            if len(ruta_para_mostrar) >= 2:
                line_weight = max(2, min(8, int(route.get('amount', 0) / 25000) + 2))
                AntPath(locations=ruta_para_mostrar, color="red", weight=line_weight, opacity=0.8, delay=800, dash_array=[10, 20], pulse_color='#FFFFFF', tooltip=f"<b>{route['from']} → {route['to']}</b><br>Monto: ${route.get('amount', 0):,.2f}<br>Viajes: {int(route.get('trips', 0))}").add_to(mapa_diario)
        except Exception as e:
            print(f"  (Error creando AntPath para {route.get('from')} a {route.get('to')}: {e})")
    title_html = f'''<h3 align="center" style="font-size:20px"><b>Rutas de Transferencia Optimizadas - {day_name}</b></h3>'''
    mapa_diario.get_root().html.add_child(folium.Element(title_html))
    map_filename = os.path.join(output_folder, f"mapa_rutas_animado_{day_name}.html")
    mapa_diario.save(map_filename)
    print(f"  ✅ Mapa para {day_name} guardado en: {map_filename}")

# ==============================================================================
# SECCIÓN 4: LÓGICA PRINCIPAL DEL DASHBOARD
# (La mayoría de las funciones aquí no cambian, el cambio importante está en
# run_optimization_and_generate_hub)
# ==============================================================================
def get_insights_from_gemini(day_results, historical_costs, total_cash_moved_so_far_weekly):
    # (Sin cambios)
    print(f"🤖 Generating AI insights for {day_results['day']} (Gemini simulation)...")
    if day_results['status'] != 'Optimal': return "<h4>AI Analysis Unavailable</h4><p>Optimization for this day did not yield a feasible solution.</p>"
    cost = day_results['variableCost']
    trips = day_results['totalTrips']
    cash_redistributed = day_results['cashRedistributed']
    cost_analysis_text = f"Optimized daily cost: <b>${cost:,.2f}</b>."
    if historical_costs:
        avg_previous_costs = sum(historical_costs) / len(historical_costs)
        cost_diff_percent = ((cost - avg_previous_costs) / avg_previous_costs) * 100 if avg_previous_costs > 0 else 0
        if cost_diff_percent > 5: cost_analysis_text += f" This is <b>{cost_diff_percent:.1f}% higher</b> than the recent average of ${avg_previous_costs:,.2f}."
        elif cost_diff_percent < -5: cost_analysis_text += f" This is <b>{abs(cost_diff_percent):.1f}% lower</b> than the recent average of ${avg_previous_costs:,.2f}, indicating improved efficiency."
        else: cost_analysis_text += f" This is in line with the recent average of ${avg_previous_costs:,.2f}."
    else: cost_analysis_text += " This is the first day of analysis, no historical trend available yet."
    route_analysis_text = f"A total of <b>{trips}</b> trips were made, redistributing <b>${cash_redistributed:,.2f}</b>."
    if day_results['routes']:
        main_route = day_results['routes'][0]
        route_analysis_text += f"<br>The key transfer was <b>${main_route['amount']:,.2f}</b> from <b>{main_route['from']}</b> to <b>{main_route['to']}</b>."
    elif trips > 0: route_analysis_text += "<br>Cash movements primarily involved central consolidation."
    else: route_analysis_text = "No cash redistribution trips were necessary today."
    savings_breakdown_text = "<h5>Estimated Savings Breakdown:</h5>"
    if trips > 0:
        factor_more_trips, factor_trip_inefficiency = 1.5, 1.3
        optimized_cost_per_trip = cost / trips
        baseline_trips = trips * factor_more_trips
        baseline_cost_per_trip_calc = optimized_cost_per_trip * factor_trip_inefficiency
        baseline_total_cost = baseline_trips * baseline_cost_per_trip_calc
        estimated_savings = baseline_total_cost - cost
        if estimated_savings > 0.01:
            savings_breakdown_text += (f"<p>By optimizing, an estimated <b>${estimated_savings:,.2f}</b> was saved.</p>" f"<ul><li>Projected unoptimized cost: <b>${baseline_total_cost:,.2f}</b></li>" f"<li>Actual optimized cost: <b>${cost:,.2f}</b></li>" f"<li><b>Estimated Net Savings: ${estimated_savings:,.2f}</b></li></ul>")
            roi_savings = (estimated_savings / cost) * 100 if cost > 0 else 0
            if roi_savings > 0: savings_breakdown_text += f"<p>This represents a <b>{roi_savings:.1f}% return</b> on logistics spending.</p>"
        else: savings_breakdown_text += "<p>Operation is highly efficient. Further significant savings are minimal.</p>"
    else: savings_breakdown_text = "<p>No physical cash transport trips were made.</p>"
    ganancias_clarification = ("<p style='font-size:0.85em; color: #444; margin-top:15px;'><i><b>Note:</b> Savings are logistics efficiencies.</i></p>")
    return (f"<h4>AI-Powered Insights for {day_results['day']}</h4>" f"<h5>Cost Analysis:</h5><p>{cost_analysis_text}</p>" f"<h5>Route & Cash Flow Efficiency:</h5><p>{route_analysis_text}</p>" f"{savings_breakdown_text}{ganancias_clarification}")

def parse_user_provided_results(text_data, tienda_names_ordered, distance_matrix_ordered):
    # (Sin cambios)
    all_day_results = {}
    day_pattern = re.compile(r"Resultados para el dia (\w+):")
    cost_pattern = re.compile(r"Los costos son:\s*([\d.]+)")
    viajes_pattern = re.compile(r"Cantidad_de_viajes_t_(\d+)_(\d+)\s*=\s*([\d.]+)")
    dinero_pattern = re.compile(r"Dinero_x_(\d+)_(\d+)\s*=\s*([\d.]+)")
    transferencias_pattern = re.compile(r"Transferencias_Electrónicas_y_(\d+)\s*=\s*([\d.]+)")
    day_blocks = day_pattern.split(text_data)[1:] 
    for i in range(0, len(day_blocks), 2):
        day_name = day_blocks[i]
        content = day_blocks[i+1]
        current_day_data = {'status': 'Optimal', 'variableCost': 0.0, 'totalTrips': 0, 'cashRedistributed': 0.0,'routes': [], 'cost_breakdown': {'distancia': 0.0, 'seguro': 0.0, 'electronico': 0.0},'raw_t': {}, 'raw_x': {}, 'raw_y': {}}
        cost_match = cost_pattern.search(content)
        if cost_match: current_day_data['variableCost'] = float(cost_match.group(1))
        for match in viajes_pattern.finditer(content):
            idx_from, idx_to, val = int(match.group(1)), int(match.group(2)), float(match.group(3))
            current_day_data['raw_t'][f"({idx_from},{idx_to})"] = val 
            current_day_data['totalTrips'] += int(val)
        for match in dinero_pattern.finditer(content):
            idx_from, idx_to, val = int(match.group(1)), int(match.group(2)), float(match.group(3))
            current_day_data['raw_x'][f"({idx_from},{idx_to})"] = val 
            current_day_data['cashRedistributed'] += val
            num_trips = int(current_day_data['raw_t'].get(f"({idx_from},{idx_to})", 1.0 if val > 0 else 0.0))
            if val > 0.01:
                 if idx_from < len(tienda_names_ordered) and idx_to < len(tienda_names_ordered):
                    current_day_data['routes'].append({'from': tienda_names_ordered[idx_from], 'to': tienda_names_ordered[idx_to], 'amount': round(val, 2), 'trips': num_trips})
                 else:
                    print(f"⚠️ Warning: Index out of bounds for tienda_names_ordered when creating route for {day_name}. From: {idx_from}, To: {idx_to}")
        for match in transferencias_pattern.finditer(content):
            idx, val = int(match.group(1)), float(match.group(2))
            current_day_data['raw_y'][str(idx)] = val 
        current_day_data['routes'] = sorted(current_day_data['routes'], key=lambda r: r['amount'], reverse=True)
        cost_dist_calc = 0
        for key_str, trips_val in current_day_data['raw_t'].items():
            try:
                indices = tuple(map(int, key_str.strip("()").split(',')))
                idx_from, idx_to = indices[0], indices[1]
                if 0 <= idx_from < len(distance_matrix_ordered) and 0 <= idx_to < len(distance_matrix_ordered[0]):
                     cost_dist_calc += 25 * distance_matrix_ordered[idx_from][idx_to] * trips_val
                else:
                    print(f"⚠️ Warning: Index out of bounds (dist_matrix) for t_{idx_from}_{idx_to} on {day_name}")
            except ValueError:
                print(f"⚠️ Warning: Could not parse key {key_str} for raw_t on {day_name}")
        cost_seg_calc = sum(0.003 * amount for amount in current_day_data['raw_x'].values())
        cost_elec_calc = sum(0.001 * amount for amount in current_day_data['raw_y'].values())
        current_day_data['cost_breakdown'] = {'distancia': round(cost_dist_calc, 2), 'seguro': round(cost_seg_calc, 2), 'electronico': round(cost_elec_calc, 2)}
        all_day_results[day_name] = current_day_data
    return all_day_results

# --- CAMBIO IMPORTANTE AQUÍ ---
def run_optimization_and_generate_hub():
    print("\n--- Initializing Street Map Engine (OSMnx) ---")
    cargar_o_descargar_grafo_osmnx()
    if MAP_LIBS_AVAILABLE and OSMNX_GRAPH is None:
        print("\n🚨 ATENCIÓN: El grafo de calles no se pudo cargar. Los mapas usarán líneas rectas. Revisa los errores.")
    print("--- Street Map Engine Ready ---")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    try:
        dist_matrix_df = pd.read_csv(FILE_PATHS["dist_matrix"], index_col=0)
        dist_matrix_df.columns = dist_matrix_df.columns.str.strip()
        dist_matrix_df.index = dist_matrix_df.index.str.strip()
        tienda_names_ordered = dist_matrix_df.index.tolist()
        distance_matrix_ordered = dist_matrix_df.values.tolist()
        print(f"✅ Loaded {FILE_PATHS['dist_matrix']}: {len(tienda_names_ordered)} stores.")
    except Exception as e:
        print(f"🚨 ERROR loading {FILE_PATHS['dist_matrix']}: {e}"); return

    try:
        coor_df = pd.read_csv(FILE_PATHS["coordinates"], skipinitialspace=True)
        coor_df.columns = coor_df.columns.str.strip()
        for col in coor_df.select_dtypes(include=['object']).columns:
            coor_df[col] = coor_df[col].str.strip()
        coordenadas_map = {}
        for _, row in coor_df.iterrows():
            try:
                lat = float(str(row['Latitud']).strip())
                lng = float(str(row['Longitud']).strip())
                coordenadas_map[row['Tienda']] = {"lat": lat, "lng": lng}
            except (ValueError, KeyError) as e:
                 print(f"⚠️ Warning: Coords parse error for row: {row.to_dict()}. Error: {e}")
        print(f"✅ Loaded {FILE_PATHS['coordinates']}: {len(coordenadas_map)} coordinate entries.")
    except Exception as e:
        print(f"🚨 ERROR loading {FILE_PATHS['coordinates']}: {e}"); return
    
    tienda_locations_frontend = {}
    default_lat, default_lng = 20.6597, -103.3496
    for nombre_canonico in tienda_names_ordered:
        coords = coordenadas_map.get(nombre_canonico)
        if not coords:
            for coor_name, coor_val in coordenadas_map.items():
                if nombre_canonico.lower() == coor_name.lower():
                    coords = coor_val
                    break
        if coords:
            tienda_locations_frontend[nombre_canonico] = coords
        else:
            tienda_locations_frontend[nombre_canonico] = { "lat": default_lat, "lng": default_lng }
    print(f"✅ Frontend locations prepared: {len(tienda_locations_frontend)} stores.")

    all_results_parsed = parse_user_provided_results(USER_PROVIDED_RESULTS, tienda_names_ordered, distance_matrix_ordered)
    historical_costs_buffer_ia, total_cash_moved_weekly, processed_all_results_frontend = deque(maxlen=2), 0, {}

    for day in days:
        if day in all_results_parsed:
            day_data = all_results_parsed[day]
            
            # --- NUEVO PASO: CALCULAR RUTAS POR CALLES PARA EL DASHBOARD ---
            print(f"  -> Pre-calculando rutas por calles para el dashboard de {day}...")
            for route_info in day_data.get('routes', []):
                loc_from_coords = tienda_locations_frontend.get(route_info['from'])
                loc_to_coords = tienda_locations_frontend.get(route_info['to'])
                
                path_coords = None
                if loc_from_coords and loc_to_coords:
                    path_coords = obtener_coordenadas_ruta_calle(
                        loc_from_coords['lat'], loc_from_coords['lng'],
                        loc_to_coords['lat'], loc_to_coords['lng']
                    )
                
                # Formatear para Google Maps (lista de objetos {lat, lng})
                if path_coords:
                    route_info['path'] = [{'lat': lat, 'lng': lng} for lat, lng in path_coords]
                else:
                    # Si falla, se deja vacío. El JS dibujará una línea recta.
                    route_info['path'] = None 
            # --- FIN DEL NUEVO PASO ---
            
            result_frontend = { 'day': day, 'status': day_data.get('status', 'Optimal'), 'variableCost': round(day_data.get('variableCost', 0.0), 2), 'totalTrips': day_data.get('totalTrips', 0), 'cashRedistributed': round(day_data.get('cashRedistributed', 0.0), 2), 'routes': day_data.get('routes', []), 'cost_breakdown': day_data.get('cost_breakdown', {}), 'raw_t': day_data.get('raw_t', {}), 'raw_x': day_data.get('raw_x', {}), 'raw_y': day_data.get('raw_y', {}) }
            result_frontend['gemini_insight'] = get_insights_from_gemini(result_frontend, list(historical_costs_buffer_ia), total_cash_moved_weekly)
            if result_frontend['status'] == 'Optimal':
                historical_costs_buffer_ia.append(result_frontend['variableCost'])
                total_cash_moved_weekly += result_frontend['cashRedistributed']
            processed_all_results_frontend[day] = result_frontend
            print(f"  > {day}: Processed. Cost: ${result_frontend['variableCost']:,.2f}")
        else:
            processed_all_results_frontend[day] = {'status': 'Data_Not_Provided', 'day': day, 'variableCost': 0, 'totalTrips':0, 'cashRedistributed':0, 'routes':[], 'raw_t':{}, 'raw_x':{}, 'raw_y':{}, 'gemini_insight': f'<h4>AI Analysis Unavailable for {day}</h4><p>Data not provided.</p>'}
            print(f"  > {day}: Data not in parsed results.")
    
    methodology = {"steps": [{"step": "1. Data Setup", "description": "Loaded store distances, coordinates, and pre-calculated optimization results."}, {"step": "2. Route Calculation", "description": "Used OSMnx to calculate street-level routes between stores for realistic visualization."}, {"step": "3. Data Processing & AI", "description": "Parsed daily results, structured data, and generated AI-simulated insights for each day."}, {"step": "4. Frontend Data Assembly", "description": "Aggregated all data, including calculated street paths, for dashboard injection."}, {"step": "5. Visualization", "description": "Generated an interactive dashboard with Google Maps displaying street-level routes, KPIs, and detailed analysis."}]}
    suppositions = {"coppel": ["Cash payments for 'abonos'.", "15% initial cash for credit sales (in payment data).", "Excess cash to central office electronically.", "Min. $150,000 per store for loans/credits.", "Min. $150,000 covers change needs."],"team": ["USER_PROVIDED_RESULTS are optimal.", "CoppelCoor.csv coordinates are accurate after cleaning.", "dist_matrix_final.csv distances are accurate.", "Store order from dist_matrix_final.csv is canonical."]}
    optimization_model = {"parameters": [{"name": "d[i][j]", "description": "Distance (km) from dist_matrix_final.csv."},{"name": "C_viaje", "description": "Truck capacity ($100,000/trip)."}, {"name": "L_max", "description": "Max cash/store ($250,000)."}, {"name": "E_min", "description": "Min cash/store ($150,000)."}],"variables": [{"name": "x[i][j]", "description": "Cash: store i to j."},{"name": "t[i][j]", "description": "#Trips: store i to j."},{"name": "y[i]", "description": "Electronic transfer: store i to central."}],"objective": "Min Total Costs: 25*dist*trips + 0.3%*cash_transferred + 0.1%*e-transfers.","constraints": ["Net cash flow/store ≤ $250K, ≥ $150K.", "E-transfers ≥ 30% cash sales (hypothetical).", "Cash transfers ≤ $100K * #trips." ]}
    
    weekly_cost_sum = sum(r['variableCost'] for r in processed_all_results_frontend.values() if r.get('status') == 'Optimal')
    weekly_trips_sum = sum(r['totalTrips'] for r in processed_all_results_frontend.values() if r.get('status') == 'Optimal')
    weekly_savings = sum(((r['totalTrips']*1.5)*(r['variableCost']/r['totalTrips']*1.3) - r['variableCost']) for r in processed_all_results_frontend.values() if r.get('status')=='Optimal' and r['totalTrips']>0 and r['variableCost']>0)
    results_summary = {"weekly_cost": weekly_cost_sum, "weekly_trips": weekly_trips_sum, "weekly_cash_moved": total_cash_moved_weekly, "weekly_savings": weekly_savings, "impact": f"Optimized cash flow achieving an estimated <b>${weekly_savings:,.2f}</b> in weekly savings vs. non-optimized scenario, enhancing operational efficiency."}

    final_data_for_frontend = { 'results': processed_all_results_frontend, 'locations': tienda_locations_frontend, 'store_names_ordered': tienda_names_ordered, 'methodology': methodology, 'suppositions': suppositions, 'optimization_model': optimization_model, 'results_summary': results_summary }

    print("\n🎨 Generating main dashboard...")
    try:
        with open(FILE_PATHS["dashboard_template"], 'r', encoding='utf-8') as f: html_template = f.read()
    except FileNotFoundError: print(f"🚨 ERROR: {FILE_PATHS['dashboard_template']} not found."); return
    
    html_output = html_template.replace("YOUR_GOOGLE_MAPS_API_KEY", GOOGLE_MAPS_API_KEY)
    html_output = html_output.replace("'YOUR_DATA_HERE'", json.dumps(final_data_for_frontend, indent=2, ensure_ascii=False)) 
    
    output_dashboard_file = FILE_PATHS["output_dashboard"]
    with open(output_dashboard_file, 'w', encoding='utf-8') as f: f.write(html_output)
    print(f"🎉 Success! Dashboard: {output_dashboard_file}")

    if MAP_LIBS_AVAILABLE:
        print("\n🗺️  Generating individual animated route maps...")
        output_map_folder = FILE_PATHS["output_maps_folder"]
        if not os.path.exists(output_map_folder):
            os.makedirs(output_map_folder)
            print(f"  Created '{output_map_folder}' directory.")
        idx_to_store_names = {i: name for i, name in enumerate(tienda_names_ordered)}
        for day, result_data in processed_all_results_frontend.items():
            if result_data.get('status') == 'Optimal' and result_data.get('routes'):
                generate_animated_map(day, result_data, tienda_locations_frontend, idx_to_store_names, output_folder=output_map_folder)
            else:
                print(f"  Skipping map for {day} (no optimal routes or data).")
    
    webbrowser.open('file://' + os.path.realpath(output_dashboard_file))


# ==============================================================================
# SECCIÓN 5: PUNTO DE ENTRADA
# ==============================================================================
if __name__ == '__main__':
    if GOOGLE_MAPS_API_KEY == "TU_API_KEY_AQUI" or not GOOGLE_MAPS_API_KEY:
        print("\n⚠️ Warning: Google Maps API Key not configured.")
    
    essential_files_to_check = [FILE_PATHS["dist_matrix"], FILE_PATHS["coordinates"], FILE_PATHS["dashboard_template"]]
    
    missing_files = [f for f in essential_files_to_check if not os.path.exists(f)]
    if not missing_files:
        run_optimization_and_generate_hub()
    else:
        print(f"\n🚨 ERROR: Faltan archivos esenciales. No se encontraron en las rutas especificadas:")
        for f in missing_files:
            print(f"  - {f}")