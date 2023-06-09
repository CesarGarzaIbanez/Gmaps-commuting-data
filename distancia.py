import pandas as pd
import googlemaps as gm
import datetime as dt


# Funcion para crear en el dataframe las columnas necesarias (Estan definidas 10)
def dfExt(times):
    i = 0
    while i < times:
        df.loc[i,f'distancia_caminando_{i+1}'] = '';
        df.loc[i,f'duracion_caminando_{i+1}'] = '';
        df.loc[i,f'distancia_camion_{i+1}'] = '';
        df.loc[i,f'duracion_camion_{i+1}'] = '';
        df.loc[i,f'ruta_{i+1}'] = '';
        i+=1;


# API GOOGLE
token = ''

# LEER ARCHIVO DE EXCEL, **** AQUI METES TU ARCHIVO ENTRE LAS COMILLAS, NO QUITES LA 'r' *****
archivo = r"data copy.csv"

# CREACION DEL DATAFRAME CON PANDAS PARA LEER EL ARCHIVO
excel = pd.DataFrame(pd.read_csv(archivo, encoding = 'utf8'))
excel.columns = ['id', 'fecha', 'tiempo', 'hora', 'minuto', 'TipoEnc', 'origen_municipio', 'origen_colonia','origen_estado', 'LugarDest', 'destino_municipio', 'destino_colonia']

# CONEXIÓN CON LA API
gmaps = gm.Client(key=token)

#TABLA DESTINO
df = pd.DataFrame([],columns = ['id', 'status', 'origen', 'destino','distancia_total_metros','duracion_total'])
# 10 columnas por cada parametro para poder visualizarla en orden
dfExt(10)

df_1 = df.copy();

df_2 = df.copy();

df_3 = df.copy();

df_4 = df.copy();


# CICLO PARA RECORRER TODAS LAS ENTRADAS DEL ARCHIVO
for i in excel.index:
    # COMBINAR EL ORIGEN Y DESTINO EN STRINGS PARA LEERLOS CON DIRECTIONS DE GMAMPS
    origen = str(excel['origen_colonia'][i] + ',' + excel['origen_municipio'][i] + ',' + excel['origen_estado'][i])
    destino = str(excel['destino_colonia'][i] + ',' + excel['destino_municipio'][i])

    #LEECTURA DE LA HORA Y TRANSFORMACION A UNIDAD DE TIEMPO UNIX_TIMESTAMP(SEGUNDOS QUE HAN PASADO DESDE 1970)
    hora = excel['hora'][i]
    minuto = excel['minuto'][i]
    tiempo = dt.datetime.now()
    tiempo = tiempo.replace(hour = hora, minute = minuto, second=0, microsecond=0)
    tiempo_New = dt.datetime.strptime(tiempo.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    unix_Timestamp = int(tiempo_New.timestamp());

    # TRY POR SI OCURRE UN ERROR NO DETENER LA EJECUCIÓN
    try:
        # 
        directions = gmaps.directions(origen, destino, mode='transit', transit_mode='bus',alternatives = True);

        # REINICIO DE INCREMENTADORES
        y=0
        alt = 1;

        # ID
        df_1.loc[i,'id'] = excel['id'][i];
        df_2.loc[i,'id'] = excel['id'][i];
        df_3.loc[i,'id'] = excel['id'][i];
        df_4.loc[i,'id'] = excel['id'][i];
        # Origen
        df_1.loc[i,'origen'] = origen;
        df_2.loc[i,'origen'] = origen;
        df_3.loc[i,'origen'] = origen;
        df_4.loc[i,'origen'] = origen;
        # Destino
        df_1.loc[i,'destino'] = destino;
        df_2.loc[i,'destino'] = destino;
        df_3.loc[i,'destino'] = destino;
        df_4.loc[i,'destino'] = destino;

        # En caso de estar vacio
        if (directions == []):
            # Estatus de Error
            df_1.loc[i,'status'] = 'Error';
            df_2.loc[i,'status'] = 'Error';
            df_3.loc[i,'status'] = 'Error';
            df_4.loc[i,'status'] = 'Error';
            continue;
        
        # Definicion de Estatus Correcto
        df_1.loc[i,'status'] = 'Correcto';
        df_2.loc[i,'status'] = 'Correcto';
        df_3.loc[i,'status'] = 'Correcto';
        df_4.loc[i,'status'] = 'Correcto';

        # Iteracion de alternativas
        for j in directions:
            
            x=0
            z=1

            if alt == 1:
            # Distancia total
                df_1.loc[i,'distancia_total_metros'] = directions[y]['legs'][0]['distance']['value'];
                # Duracion total
                df_1.loc[i,'duracion_total'] = directions[y]['legs'][0]['duration']['text'];
                # Iteracion en busca de los pasos del camino
                for k in directions[y]['legs'][0]['steps']:

                    # Identifica si es en caminando
                    if (directions[y]['legs'][0]['steps'][x]['travel_mode']) == 'WALKING':
                        df_1.loc[i,f'distancia_caminando_{z}'] = directions[y]['legs'][0]['steps'][x]['distance']['value'];
                        df_1.loc[i,f'duracion_caminando_{z}'] = directions[y]['legs'][0]['steps'][x]['duration']['text'];


                    # Identifica si es en transporte publico (camion)
                    elif (directions[y]['legs'][0]['steps'][x]['travel_mode']) == 'TRANSIT':
                        df_1.loc[i,f'distancia_camion_{z}'] = directions[y]['legs'][0]['steps'][x]['distance']['value'];
                        df_1.loc[i,f'duracion_camion_{z}'] = directions[y]['legs'][0]['steps'][x]['duration']['text'];
                        df_1.loc[i,f'ruta_{z}'] = directions[y]['legs'][0]['steps'][x]['transit_details']['line']['name'];
                    df_1.to_csv('final_1.csv', index=False, encoding='utf-8')
                    x = x+1 
                    z=z+1
            elif alt == 2:
            # Distancia total
                df_2.loc[i,'distancia_total_metros'] = directions[y]['legs'][0]['distance']['value'];
                # Duracion total
                df_2.loc[i,'duracion_total'] = directions[y]['legs'][0]['duration']['text'];
                # Iteracion en busca de los pasos del camino
                for k in directions[y]['legs'][0]['steps']:

                    # Identifica si es en caminando
                    if (directions[y]['legs'][0]['steps'][x]['travel_mode']) == 'WALKING':
                        df_2.loc[i,f'distancia_caminando_{z}'] = directions[y]['legs'][0]['steps'][x]['distance']['value'];
                        df_2.loc[i,f'duracion_caminando_{z}'] = directions[y]['legs'][0]['steps'][x]['duration']['text'];


                    # Identifica si es en transporte publico (camion)
                    elif (directions[y]['legs'][0]['steps'][x]['travel_mode']) == 'TRANSIT':
                        df_2.loc[i,f'distancia_camion_{z}'] = directions[y]['legs'][0]['steps'][x]['distance']['value'];
                        df_2.loc[i,f'duracion_camion_{z}'] = directions[y]['legs'][0]['steps'][x]['duration']['text'];
                        df_2.loc[i,f'ruta_{z}'] = directions[y]['legs'][0]['steps'][x]['transit_details']['line']['name'];
                    df_2.to_csv('final_2.csv', index=False, encoding='utf-8')
                    x = x+1 
                    z=z+1
            elif alt == 3:
            # Distancia total
                df_3.loc[i,'distancia_total_metros'] = directions[y]['legs'][0]['distance']['value'];
                # Duracion total
                df_3.loc[i,'duracion_total'] = directions[y]['legs'][0]['duration']['text'];
                # Iteracion en busca de los pasos del camino
                for k in directions[y]['legs'][0]['steps']:

                    # Identifica si es en caminando
                    if (directions[y]['legs'][0]['steps'][x]['travel_mode']) == 'WALKING':
                        df_3.loc[i,f'distancia_caminando_{z}'] = directions[y]['legs'][0]['steps'][x]['distance']['value'];
                        df_3.loc[i,f'duracion_caminando_{z}'] = directions[y]['legs'][0]['steps'][x]['duration']['text'];


                    # Identifica si es en transporte publico (camion)
                    elif (directions[y]['legs'][0]['steps'][x]['travel_mode']) == 'TRANSIT':
                        df_3.loc[i,f'distancia_camion_{z}'] = directions[y]['legs'][0]['steps'][x]['distance']['value'];
                        df_3.loc[i,f'duracion_camion_{z}'] = directions[y]['legs'][0]['steps'][x]['duration']['text'];
                        df_3.loc[i,f'ruta_{z}'] = directions[y]['legs'][0]['steps'][x]['transit_details']['line']['name'];
                    df_3.to_csv('final_3.csv', index=False, encoding='utf-8')   
                    x = x+1 
                    z=z+1
            elif alt == 4:
                 # Distancia total
                df_4.loc[i,'distancia_total_metros'] = directions[y]['legs'][0]['distance']['value'];
                # Duracion total
                df_4.loc[i,'duracion_total'] = directions[y]['legs'][0]['duration']['text'];
                # Iteracion en busca de los pasos del camino
                for k in directions[y]['legs'][0]['steps']:

                    # Identifica si es en caminando
                    if (directions[y]['legs'][0]['steps'][x]['travel_mode']) == 'WALKING':
                        df_4.loc[i,f'distancia_caminando_{z}'] = directions[y]['legs'][0]['steps'][x]['distance']['value'];
                        df_4.loc[i,f'duracion_caminando_{z}'] = directions[y]['legs'][0]['steps'][x]['duration']['text'];


                    # Identifica si es en transporte publico (camion)
                    elif (directions[y]['legs'][0]['steps'][x]['travel_mode']) == 'TRANSIT':
                        df_4.loc[i,f'distancia_camion_{z}'] = directions[y]['legs'][0]['steps'][x]['distance']['value'];
                        df_4.loc[i,f'duracion_camion_{z}'] = directions[y]['legs'][0]['steps'][x]['duration']['text'];
                        df_4.loc[i,f'ruta_{z}'] = directions[y]['legs'][0]['steps'][x]['transit_details']['line']['name'];
                    df_4.to_csv('final_4.csv', index=False, encoding='utf-8')
                    x = x+1 
                    z=z+1
            alt = alt+1
            y= y+1

# Estatus de error
    except gm.exceptions.ApiError:
        df_1.loc[i,'status'] = 'Error';
        df_2.loc[i,'status'] = 'Error';
        df_3.loc[i,'status'] = 'Error';
        df_4.loc[i,'status'] = 'Error';
    


   



