from tkinter import *
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

# Función para leer el archivo Excel y obtener el DataFrame correspondiente
def leer_ruta(ruta, tabla):
    df = pd.read_excel(ruta, sheet_name=tabla)
    return df

# Especificar la ruta del archivo Excel
ruta = "C:/Users/Lenovo/Downloads/Gomez_Huarancca_Tamariz_Torres_Base de datos _Exportaciones.xlsx"

# Leer las diferentes hojas del archivo Excel en DataFrames
exportaciones = leer_ruta(ruta, "Exportaciones")
categoria3 = leer_ruta(ruta, "Categoria3")
via = leer_ruta(ruta, "Via")
puerto = leer_ruta(ruta, "Puerto")
mercancia = leer_ruta(ruta, "Mercancia")
categoria1 = leer_ruta(ruta, "Categoria1")
destinos = leer_ruta(ruta, "Destino")
regiones = leer_ruta(ruta, "Region")
sector = leer_ruta(ruta, "Sector")
subsector = leer_ruta(ruta, "Subsector")
categoria2 = leer_ruta(ruta, "Categoria2")
partida = leer_ruta(ruta, "Partida")

# Integrar los datos de las diferentes tablas en un DataFrame unificado
export_region = pd.merge(exportaciones, regiones, on = "id_region", how="left")
export_destino = pd.merge(export_region, destinos,on = "id_destino", how="left")
export_mercancia = pd.merge(export_destino, mercancia,on  = "id_mercancia", how="left")
export_via = pd.merge(export_mercancia, via,on = "id_via", how="left")
export_puerto = pd.merge(export_via, puerto, on = "id_puerto", how="left")
export_partida = pd.merge(export_puerto, partida,on = "cod_Partida", how="left")
export_subsector = pd.merge(export_partida, subsector,on = "id_subsector", how="left")
export_cat3 = pd.merge(export_subsector, categoria3, on = "id_cat3", how="left")
export_cat2 = pd.merge(export_cat3, categoria2,on = "id_cat2", how="left")
export_cat1 = pd.merge(export_cat2, categoria1, on = "id_cat1", how="left")
database = pd.merge(export_cat1, sector,on = "id_sector", how="left")

# Función para generar y mostrar el gráfico
def grafico_año_region():
    # Filtrar los datos para los años 2021 y 2022
    years = [2021, 2022]
    database_filtered = database[database['Año'].isin(years)]

    # Convertir los US$ FOB a millones
    database_filtered['US$ FOB (Millones)'] = database_filtered['US$ FOB'] / 1e6

    # Agrupar por Año, Región y Sector, y sumar los US$ FOB en millones
    df_exportaciones = database_filtered.groupby(['Año', 'Región', 'Sector'])['US$ FOB (Millones)'].sum().reset_index()

    # Definir los colores para cada sector
    sector_colors = {
        'MINERIA TRADICIONAL': 'rgb(255, 0, 0)',    # Rojo
        'PESCA TRADICIONAL': 'rgb(255, 255, 0)',   # Amarillo
        'AGRO TRADICIONAL': 'rgb(255, 182, 193)'   # Rosado
    }

    # Definir los colores para cada año
    year_colors = {
        2021: 'rgb(31, 120, 180)',  # Azul
        2022: 'rgb(50, 205, 50)'    # Verde
    }

    # Crear la figura interactiva con Plotly
    fig = go.Figure()

    # Añadir trazas de barras para cada combinación de año y sector
    for year in years:
        for sector_name in df_exportaciones['Sector'].unique():
            data_filtered = df_exportaciones[(df_exportaciones['Año'] == year) & (df_exportaciones['Sector'] == sector_name)]
            fig.add_trace(go.Bar(
                x=data_filtered['Región'],
                y=data_filtered['US$ FOB (Millones)'],
                name=f'{sector_name}, {year}',
                marker_color=year_colors[year],  # Color según el año
                hovertemplate=f'Región: %{{x}}<br>US$ FOB: %{{y:,.2f}} millones<br>Año: {year}<br>Sector: {sector_name}<extra></extra>',
                textposition='outside',
                texttemplate='%{y:,.2f}',
                visible=True  # Inicialmente mostrar todas las barras
            ))

    # Crear las combinaciones de botones para filtrar tanto por año como por sector
    buttons = []
    for year in years + ['Ambos Años']:
        for sector_name in df_exportaciones['Sector'].unique().tolist() + ['Todos los Sectores']:
            visible = [
                (trace.name.endswith(f', {year}') if year != 'Ambos Años' else True) and 
                (trace.name.startswith(sector_name) if sector_name != 'Todos los Sectores' else True)
                for trace in fig.data
            ]
            buttons.append(dict(
                label=f'{sector_name}, {year}',
                method='update',
                args=[{'visible': visible},
                      {'title': f'Exportaciones totales en US$ FOB por región{f" para el año {year}" if year != "Ambos Años" else ""}{f" para el sector {sector_name}" if sector_name != "Todos los Sectores" else ""}'}
                ]
            ))

    # Configurar el diseño del gráfico con los botones de filtro
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=buttons,
                direction='down',
                showactive=True,
                x=1.1,  # Posición ajustada a la derecha
                xanchor='right',  # Ajuste al borde derecho
                y=1.15,  # Posición ajustada arriba
                yanchor='top'  # Ajuste al borde superior
            )
        ],
        title='Exportaciones totales en US$ FOB por región (2021 y 2022)',
        xaxis_title='Región',
        yaxis_title='US$ FOB (Millones)',
        yaxis=dict(tickformat='.2f', dtick=300),  # Ajuste de formato y espaciado en el eje y
        barmode='group'
    )

    # Ajustar las propiedades de la leyenda para hacerla dinámica
    fig.update_layout(
        legend=dict(
            title='',
            orientation='v',  # Orientación vertical
            x=1.05,  # Posición ajustada a la derecha
            xanchor='right',  # Ajuste al borde derecho
            y=0.95,  # Ajuste vertical
            yanchor='top',
            itemsizing='constant',
            font=dict(size=10)
        )
    )

    # Renderizar el gráfico en la consola de Spyder
    plot(fig)

    # Alternativamente, guardar el gráfico como archivo HTML interactivo y abrirlo manualmente
    fig.write_html('exportaciones_totales_region.html')

# Función para buscar mascota
def buscar_mascota():
        
    # Convertir los US$ FOB a millones
    database['US$ FOB (Millones)'] = database['US$ FOB'] / 1e6
    
    # Agrupar por Sector y Subsector, y sumar los US$ FOB en millones
    df_exportaciones_subsector = database.groupby(['Sector', 'Subsector'])['US$ FOB (Millones)'].sum().reset_index()
    
    # Definir los colores para cada sector
    sector_colors = {
        'MINERIA TRADICIONAL': 'rgb(139, 69, 19)',    # Marrón
        'PESCA TRADICIONAL': 'rgb(64, 224, 208)',     # Turquesa
        'AGRO TRADICIONAL': 'rgb(255, 215, 0)'        # Oro
    }
    
    # Encontrar el valor máximo de US$ FOB en millones para establecer el rango del eje Y
    max_fob_value = df_exportaciones_subsector['US$ FOB (Millones)'].max()
    
    # Crear la figura interactiva con Plotly para el gráfico de Sector y Subsector
    fig_subsector = go.Figure()
    
    # Añadir trazas de barras para cada combinación de sector y subsector, ordenadas en orden descendente
    for sector_name in df_exportaciones_subsector['Sector'].unique():
        data_filtered = df_exportaciones_subsector[df_exportaciones_subsector['Sector'] == sector_name]
        data_filtered = data_filtered.sort_values(by='US$ FOB (Millones)', ascending=False)  # Ordenar de forma descendente
        fig_subsector.add_trace(go.Bar(
            x=data_filtered['Subsector'],
            y=data_filtered['US$ FOB (Millones)'],
            name=f'{sector_name}',
            marker_color=sector_colors.get(sector_name, 'rgb(128, 128, 128)'),  # Color según el sector
            hovertemplate=f'Sector: {sector_name}<br>Subsector: %{{x}}<br>US$ FOB: %{{y:,.2f}} millones<extra></extra>',
            textposition='outside',
            texttemplate='%{y:,.2f}',
            visible=True  # Inicialmente mostrar todas las barras
        ))
    
    # Crear las combinaciones de botones para filtrar por sector y subsector
    buttons_subsector = [
        dict(
            label='Exportaciones Totales',
            method='update',
            args=[{'visible': [True] * len(fig_subsector.data)},
                  {'title': 'Exportaciones totales en US$ FOB por subsector'}]
        )
    ]
    
    for sector_name in df_exportaciones_subsector['Sector'].unique():
        visible = [
            (trace.name == sector_name)
            for trace in fig_subsector.data
        ]
        label = f'{sector_name} y subsectores'
        buttons_subsector.append(dict(
            label=label,
            method='update',
            args=[{'visible': visible},
                  {'title': f'Exportaciones totales en US$ FOB para el sector {sector_name} y subsectores'}]
        ))
    
    # Configurar el diseño del gráfico con los botones de filtro para Subsector
    fig_subsector.update_layout(
        updatemenus=[
            dict(
                buttons=buttons_subsector,
                direction='down',
                showactive=True,
                x=1.1,  # Posición ajustada a la derecha
                xanchor='right',  # Ajuste al borde derecho
                y=1.15,  # Posición ajustada arriba
                yanchor='top'  # Ajuste al borde superior
            )
        ],
        title='Exportaciones totales en US$ FOB por sector y subsector',
        xaxis_title='Subsector',
        yaxis_title='US$ FOB (Millones)',
        yaxis=dict(tickformat='.2f', dtick=2000, range=[0, max_fob_value * 1.1]),  # Ajuste de formato y rango en el eje y
        barmode='group'
    )
    
    # Ajustar las propiedades de la leyenda para hacerla dinámica
    fig_subsector.update_layout(
        legend=dict(
            title='',
            orientation='v',  # Orientación vertical
            x=1.05,  # Posición ajustada a la derecha
            xanchor='right',  # Ajuste al borde derecho
            y=0.95,  # Ajuste vertical
            yanchor='top',
            itemsizing='constant',
            font=dict(size=10)
        )
    )
    
    # Renderizar el gráfico en la consola de Spyder
    plot(fig_subsector)
    
    # Guardar el gráfico como archivo HTML interactivo
    fig_subsector.write_html('exportaciones_totales_subsector.html')

# Función para actualizar datos
def grafico_año_mes():
    
    # Filtrar los datos para los años 2021 y 2022
    years = [2021, 2022]
    exportaciones = database[database['Año'].isin(years)]
    
    # Agrupar por Año, Mes y contar países únicos
    df_exportaciones_mes = exportaciones.groupby(['Año', 'Mes'])['País'].nunique().reset_index()
    
    # Sumar los valores de US$ FOB por Año y Mes
    df_exportaciones_mes['US$ FOB'] = exportaciones.groupby(['Año', 'Mes'])['US$ FOB'].sum().values / 1e6  # Convertir a millones
    
    # Crear figura interactiva con Plotly
    fig = go.Figure()
    
    # Añadir trazas de líneas para cada año
    for year in years:
        data_filtered = df_exportaciones_mes[df_exportaciones_mes['Año'] == year]
        fig.add_trace(go.Scatter(
            x=data_filtered['Mes'],
            y=data_filtered['US$ FOB'],  # No es necesario dividir por 1e6 aquí
            mode='lines+markers',
            name=f'{year}',
            hovertemplate='Año: %{customdata}<br>Mes: %{x}<br>US$ FOB: %{y:,.2f} millones<br>Número de Países: %{text}<extra></extra>',
            customdata=[year]*len(data_filtered),  # Utilizar el año correspondiente como dato personalizado
            text=data_filtered['País']  # Número de países únicos como dato en el hovertemplate
        ))
        
    # Configurar botones para alternar la visualización por año y ambos años
    buttons = [
        dict(
            label='Ambos Años',
            method='update',
            args=[{'visible': [True, True]},  # Mostrar ambas trazas
                  {'title': 'Exportaciones totales en US$ FOB por mes para ambos años'}]
        ),
        dict(
            label='2021',
            method='update',
            args=[{'visible': [True, False]},  # Mostrar solo 2021
                  {'title': 'Exportaciones totales en US$ FOB por mes para el año 2021'}]
        ),
        dict(
            label='2022',
            method='update',
            args=[{'visible': [False, True]},  # Mostrar solo 2022
                  {'title': 'Exportaciones totales en US$ FOB por mes para el año 2022'}]
        )]
    
    # Configurar el diseño del gráfico
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=buttons,
                direction='down',
                showactive=True,
                x=0.5,
                xanchor='center',
                y=1.15,
                yanchor='top'
            ),
        ],
        title='Exportaciones totales en US$ FOB por mes (2021 y 2022)',
        xaxis_title='Mes',
        yaxis_title='US$ FOB (Millones)',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        ),
        yaxis=dict(tickformat='.2f'),
        legend=dict(
            title='Año',
            x=0.95,
            xanchor='right',
            y=0.95,
            yanchor='top'
        )
    )
    
    # Mostrar el gráfico en la consola de Spyder
    plot(fig)
    
    # Alternativamente, guardar el gráfico como archivo HTML interactivo y abrirlo manualmente
    fig.write_html('exportaciones_totales_mes_2021_2022.html')

def año_pais():      
    # Filtrar los datos para los años 2021 y 2022
    years = [2021, 2022]
    database2 = database[database['Año'].isin(years)]
    
    # Convertir los US$ FOB a millones
    database2['US$ FOB (Millones)'] = database2['US$ FOB'] / 1e6
    
    # Agrupar por Año, Región y Sector, y sumar los US$ FOB en millones
    df_exportaciones = database2.groupby(['Año', 'País', 'Sector'])['US$ FOB (Millones)'].sum().reset_index()
    
    # Definir los colores para cada sector
    sector_colors = {
        'MINERIA TRADICIONAL': 'rgb(165, 42, 42)',    # Marrón
        'PESCA TRADICIONAL': 'rgb(255, 140, 0)',     # Anaranjado
        'AGRO TRADICIONAL': 'rgb(210, 105, 30)'      # Marrón más claro
    }
    
    # Definir los colores para cada año
    year_colors = {
        2021: 'rgb(160, 82, 45)',  # Marrón oscuro
        2022: 'rgb(255, 165, 0)'   # Anaranjado claro
    }
    
    # Crear la figura interactiva con Plotly
    fig = go.Figure()
    
    # Añadir trazas de barras para cada combinación de año y sector
    for year in years:
        for sector_name in df_exportaciones['Sector'].unique():
            data_filtered = df_exportaciones[(df_exportaciones['Año'] == year) & (df_exportaciones['Sector'] == sector_name)]
            data_filtered = data_filtered.sort_values(by='US$ FOB (Millones)', ascending=False).head(13)
            fig.add_trace(go.Bar(
                x=data_filtered['País'],
                y=data_filtered['US$ FOB (Millones)'],
                name=f'{sector_name}, {year}',
                marker_color=year_colors[year],  # Color según el año
                hovertemplate=f'Región: %{{x}}<br>US$ FOB: %{{y:,.2f}} millones<br>Año: {year}<br>Sector: {sector_name}<extra></extra>',
                textposition='outside',
                texttemplate='%{y:,.2f}',
                visible=True  # Inicialmente mostrar todas las barras
            ))
    
    # Crear las combinaciones de botones para filtrar tanto por año como por sector
    buttons = []
    for year in years + ['Ambos Años']:
        for sector_name in df_exportaciones['Sector'].unique().tolist() + ['Todos los Sectores']:
            visible = [
                (trace.name.endswith(f', {year}') if year != 'Ambos Años' else True) and 
                (trace.name.startswith(sector_name) if sector_name != 'Todos los Sectores' else True)
                for trace in fig.data
            ]
            buttons.append(dict(
                label=f'{sector_name}, {year}',
                method='update',
                args=[{'visible': visible},
                      {'title': f'Exportaciones totales en US$ FOB por país{f" para el año {year}" if year != "Ambos Años" else ""}{f" para el sector {sector_name}" if sector_name != "Todos los Sectores" else ""}'}
                ]
            ))
    
    # Configurar el diseño del gráfico con los botones de filtro
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=buttons,
                direction='down',
                showactive=True,
                x=1.1,  # Posición ajustada a la derecha
                xanchor='right',  # Ajuste al borde derecho
                y=1.15,  # Posición ajustada arriba
                yanchor='top'  # Ajuste al borde superior
            )
        ],
        title='Exportaciones totales en US$ FOB por país (2021 y 2022)',
        xaxis_title='País',
        yaxis_title='US$ FOB (Millones)',
        yaxis=dict(tickformat='.2f', dtick=1000),  # Ajuste de formato y espaciado en el eje y
        barmode='group'
    )
    
    # Ajustar las propiedades de la leyenda para hacerla dinámica
    fig.update_layout(
        legend=dict(
            title='',
            orientation='v',  # Orientación vertical
            x=1.05,  # Posición ajustada a la derecha
            xanchor='right',  # Ajuste al borde derecho
            y=0.95,  # Ajuste vertical
            yanchor='top',
            itemsizing='constant',
            font=dict(size=10)
        )
    )
    
    # Renderizar el gráfico en la consola de Spyder
    plot(fig)
    
    # Alternativamente, guardar el gráfico como archivo HTML interactivo y abrirlo manualmente
    fig.write_html('exportaciones_totales_país.html')
    

def variacion_entre_años():
    # Filtrar los datos para los años 2021 y 2022
    years = [2021, 2022]
    database3 = database[database['Año'].isin(years)]

    # Convertir los US$ FOB a millones
    database3['US$ FOB (Millones)'] = database3['US$ FOB'] / 1e6

    # Agrupar por Año y Región, y sumar los US$ FOB en millones
    df_exportaciones = database3.groupby(['Año', 'Región'])['US$ FOB (Millones)'].sum().reset_index()

    # Pivotar la tabla para calcular las variaciones porcentuales
    df_pivot = df_exportaciones.pivot(index='Región', columns='Año', values='US$ FOB (Millones)').reset_index()
    print(df_pivot)
    df_pivot['Variación (%)'] = ((df_pivot[2022] - df_pivot[2021]) / df_pivot[2021]) * 100

    # Crear la figura interactiva con Plotly
    fig = go.Figure()

    # Añadir traza de barras para la variación porcentual
    fig.add_trace(go.Bar(
        x=df_pivot['Región'],
        y=df_pivot['Variación (%)'],
        marker_color='rgb(31, 120, 180)',  # Color azul para las barras
        hovertemplate='Región: %{x}<br>Variación: %{y:.2f}%<extra></extra>',
        textposition='outside',
        texttemplate='%{y:.2f}%',
    ))

    # Configurar el diseño del gráfico
    fig.update_layout(
        title='Variación porcentual de las exportaciones en US$ FOB por región (2021-2022)',
        xaxis_title='Región',
        yaxis_title='Variación (%)',
        yaxis=dict(tickformat='.2f', dtick=400),  # Ajuste de formato y espaciado en el eje y
        barmode='group'
    )

    # Ajustar las propiedades de la leyenda para hacerla dinámica
    fig.update_layout(
        legend=dict(
            title='',
            orientation='v',  # Orientación vertical
            x=1.05,  # Posición ajustada a la derecha
            xanchor='right',  # Ajuste al borde derecho
            y=0.95,  # Ajuste vertical
            yanchor='top',
            itemsizing='constant',
            font=dict(size=10)
        )
    )

    # Renderizar el gráfico en la consola de Spyder
    plot(fig)

    # Alternativamente, guardar el gráfico como archivo HTML interactivo y abrirlo manualmente
    fig.write_html('variacion_exportaciones_region.html')
    

# Código principal
ventana = Tk()
ventana.title("Graficos")
ventana.geometry("400x400")

# Botón para generar el gráfico
boton_guardar = Button(ventana, text='Año y region', command=grafico_año_region)
boton_guardar.pack()


# Botones adicionales (buscar y actualizar)
boton_buscar = Button(ventana, text='Sector y subsector', command=buscar_mascota)
boton_buscar.pack()

boton_actualizar = Button(ventana, text='año mes', command=grafico_año_mes)
boton_actualizar.pack()



boton_año_pais = Button(ventana, text='año pais', command=año_pais)
boton_año_pais.pack()

boton_variacion = Button(ventana, text='variacion entre años', command=variacion_entre_años)
boton_variacion.pack()
# Iniciar el ciclo de la ventana
ventana.mainloop()