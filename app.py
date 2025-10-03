import dash
import plotly.express as px
import pandas as pd
import janitor as jan
import geopandas as gpd            
import plotly.express as px      
from dash import Dash, dcc, html 
import plotly.graph_objects as go
import json


#Carga de datos
df = pd.read_csv("Tasa_mortalidad_cancer.csv")
mapa_col= gpd.read_file("COLOMBIA\COLOMBIA.shp",encoding="latin1")

codigos_departamentos = {
    'Amazonas': '91',
    'Antioquia': '05',
    'Arauca': '81',
    'Archipiélago de San Andrés, Providencia': '88',  
    'Atlántico': '08',
    'Bogotá D.C': '11',  
    'Bolívar': '13',
    'Boyacá': '15',
    'Caldas': '17',
    'Caquetá': '18',
    'Casanare': '85',
    'Cauca': '19',
    'Cesar': '20',
    'Chocó': '27',
    'Córdoba': '23',
    'Cundinamarca': '25',
    'Guainía': '94',
    'Guaviare': '95',
    'Huila': '41',
    'La Guajira': '44',
    'Magdalena': '47',
    'Meta': '50',
    'Nariño': '52',
    'Norte de Santander': '54',
    'Putumayo': '86',
    'Quindio': '63',  
    'Risaralda': '66',
    'Santander': '68',
    'Sucre': '70',
    'Tolima': '73',
    'Valle del Cauca': '76',
    'Vaupés': '97',
    'Vichada': '99'
}

#Eliminar filas nulas y limpieza de nombres de columnas-----------------------------
df=jan.clean_names(df)
df.head()

obs_eliminar = ['Tasa de mortalidad cruda por 100.000 personas-año.  en ambos sexos. edades [080+]. cáncer de hígado. Amazonas. Antioquia. Arauca. Archipiélago de San Andrés. Providencia . Atlántico. Bogotá D.C. Bolívar. Boyacá. Caldas. Caquetá. Casanare. Cauca. Cesar. Chocó. Cundinamarca. Córdoba. Guainía. Guaviare. Huila. La Guajira. Magdalena. Meta. Nariño. Norte de Santander. Putumayo. Quindio. Risaralda. Santander. Sucre. Tolima. Valle del Cauca. Vaupés. Vichada. años 1997. 1998. 1999. 2000. 2001. 2002. 2003. 2004. 2005. 2006. 2007. 2008. 2009. 2010. 2011. 2012. 2013. 2014. 2015. 2016. 2017. 2018. 2019',
       'Tasa de mortalidad cruda por 100.000 personas-año,  en ambos sexos, edades [0 - 80+], cáncer de placenta, Amazonas, Antioquia, Arauca, Archipiélago de San Andrés, Providencia , Atlántico, Bogotá D.C, Bolívar, Boyacá, Caldas, Caquetá, Casanare, Cauca, Cesar, Chocó, Cundinamarca, Córdoba, Guainía, Guaviare, Huila, La Guajira, Magdalena, Meta, Nariño, Norte de Santander, Putumayo, Quindio, Risaralda, Santander, Sucre, Tolima, Valle del Cauca, Vaupés, Vichada, años 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019',
       'Tasa de mortalidad cruda por 100.000 personas-año,  en ambos sexos, edades [0 - 80+], cáncer de pene, Amazonas, Antioquia, Arauca, Archipiélago de San Andrés, Providencia , Atlántico, Bogotá D.C, Bolívar, Boyacá, Caldas, Caquetá, Casanare, Cauca, Cesar, Chocó, Cundinamarca, Córdoba, Guainía, Guaviare, Huila, La Guajira, Magdalena, Meta, Nariño, Norte de Santander, Putumayo, Quindio, Risaralda, Santander, Sucre, Tolima, Valle del Cauca, Vaupés, Vichada, años 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019',
       'Tasa de mortalidad cruda por 100.000 personas-año,  en ambos sexos, edades [0 - 80+], cáncer de leucemias no específicas, Amazonas, Antioquia, Arauca, Archipiélago de San Andrés, Providencia , Atlántico, Bogotá D.C, Bolívar, Boyacá, Caldas, Caquetá, Casanare, Cauca, Cesar, Chocó, Cundinamarca, Córdoba, Guainía, Guaviare, Huila, La Guajira, Magdalena, Meta, Nariño, Norte de Santander, Putumayo, Quindio, Risaralda, Santander, Sucre, Tolima, Valle del Cauca, Vaupés, Vichada, años 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019']

df['localizacion'] = df['localizacion'].replace('Archipiélago de San Andrés. Providencia', 'Archipiélago de San Andrés, Providencia')
df['tipo_de_cancer'] = df['tipo_de_cancer'].replace('Tráquea, bronquios y pulmón', 'Pulmón')

df = df.loc[~df['localizacion'].isin(obs_eliminar)]


#Creación de clave común para unión con shapefile
df['DPTO_CCDGO'] = df['localizacion'].map(codigos_departamentos)
mapa_col['DPTO_CCDGO'] = mapa_col['DPTO_CCDGO'].astype("object")
mapa_col["geometry"] = mapa_col["geometry"].simplify(0.01, preserve_topology=True)

#Resumenes estadísticos-----------------------------
resum_mama = (df[df['tipo_de_cancer'] == 'Mama'][['localizacion', '2000', '2018']])
resum_pulmon = (df[df['tipo_de_cancer'] == 'Pulmón'][['localizacion', '2000', '2018']])
resum_colon = (df[df['tipo_de_cancer'] == 'Colon'][['localizacion', '2000', '2018']])

#Creación app de dash-----------------------------

app = Dash(__name__)   
server = app.server    

#Linea temporal por departamento y tipo de cáncer---------------------------------
year_columns = [col for col in df.columns if col.isdigit() and len(col) == 4]

df_long = df.melt(
    id_vars=["localizacion", "tipo_de_cancer", "DPTO_CCDGO"],  # Incluir DPTO_CCDGO
    value_vars=year_columns,  # Especificar solo las columnas de años
    var_name="Año",
    value_name="tasa_mortalidad"  # Cambiar nombre para coincidir con tu error anterior
)

df_long["Año"] = df_long["Año"].astype(int)

#Boxplots-----------------------------

#Pulmon
df_box_pul = resum_pulmon[["2000", "2018"]].melt(
    var_name="Año", value_name="Tasa"
)
df_box_pul['localizacion'] = resum_pulmon['localizacion'].tolist() * 2

fig_box_pul = px.box(df_box_pul,x="Año",y="Tasa",color="Año",points="all", 
    title="Boxplot Tasa de mortalidad cáncer de Pulmón por 100k habitantes",
    hover_data={'localizacion': True}
)

fig_box_pul.update_layout(
    yaxis_title="Tasa por región"
)

#Mama

df_box_mama = resum_mama[["2000", "2018"]].melt(
    var_name="Año", value_name="Tasa"
)
df_box_mama['localizacion'] = resum_mama['localizacion'].tolist() * 2

fig_box_mama = px.box(df_box_mama,x="Año",y="Tasa",color="Año",points="all", 
    title="Boxplot Tasa de mortalidad cáncer de Mama por 100k habitantes",
    hover_data={'localizacion': True}
)

fig_box_mama.update_layout(
    yaxis_title="Tasa por región"
)

#Colon

df_box_colon = resum_colon[["2000", "2018"]].melt(
    var_name="Año", value_name="Tasa"
)
df_box_colon['localizacion'] = resum_colon['localizacion'].tolist() * 2

fig_box_colon = px.box(df_box_colon,x="Año",y="Tasa",color="Año",points="all", 
    title="Boxplot Tasa de mortalidad cáncer de Colon por 100k habitantes",
    hover_data={'localizacion': True}
)

fig_box_colon.update_layout(
    yaxis_title="Tasa por región"
)

years = [str(y) for y in range(2000, 2019)]

#Layout de la página-----------------------------
app.layout = html.Div([
    
    html.H1("Dashboard de Análisis", style={"textAlign": "center"}), 

    #1 parte
    html.H2("1. Tasa de mortalidad por departamento"),
    html.P("Este gráfico muestra la comparación de la tasa de mortalidad entre los diferentes departamentos en un año específico. "
           "Permite identificar cuáles regiones presentan mayores o menores niveles de mortalidad por cáncer en el periodo seleccionado."),
    dcc.Dropdown(
        id="year-dropdown-loc",
        options=[{"label": y, "value": y} for y in years],
        value="2000" 
    ),
    dcc.Graph(id="graph-bar-loc"),

    #2 parte
    html.H2("2. Tasa de mortalidad por tipo de cáncer"),
    html.P("Aquí se presenta la mortalidad según el tipo de cáncer en Colombia. "
           "Esto permite entender qué tipos de cáncer son más prevalentes en el año seleccionado."),
    dcc.Dropdown(
        id="year-dropdown-can",
        options=[{"label": y, "value": y} for y in years],
        value="2000"
    ),
    dcc.Graph(id="graph-bar-can"),

    #3 parte boxplots
    html.H2("3. Boxplots comparativos por cánceres frecuentes"),
    html.P("Los siguientes boxplots comparan la distribución de tasas de mortalidad en tres de los cánceres más frecuentes (pulmón, mama y colon), "
           "en dos momentos del tiempo (2000 vs 2018). Esto permite observar cambios en la dispersión y valores atípicos."),
    html.H3("Boxplot Tasa de mortalidad cáncer de Pulmón (2000 vs 2018)"),
    dcc.Graph(figure=fig_box_pul),  # Mostramos el boxplot

    html.H3("Boxplot Tasa de mortalidad cáncer de Mama (2000 vs 2018)"),
    dcc.Graph(figure=fig_box_mama),  # Mostramos el boxplot

    html.H3("Boxplot Tasa de mortalidad cáncer de Colon (2000 vs 2018)"),
    dcc.Graph(figure=fig_box_colon),  # Mostramos el boxplot

    #4 parte Grafica de linea temporal
    html.H2("4. Evolución temporal por departamento y tipo de cáncer"),
    html.P("La línea de tiempo permite seguir la evolución de la mortalidad en un departamento y tipo de cáncer específico. "
           "Esto facilita analizar tendencias y posibles reducciones o aumentos en el tiempo."),
    html.Div([ 
        html.Div([
            html.Label("Selecciona departamento:"),
            dcc.Dropdown(
                id="dropdown-depto",
                options=[{"label": loc, "value": loc} for loc in df_long["localizacion"].unique()],
                value=df_long["localizacion"].unique()[0],
                clearable=False
            )
        ], style={"width": "45%", "display": "inline-block"}),

        html.Div([
            html.Label("Selecciona tipo de cáncer:"),
            dcc.Dropdown(
                id="dropdown-cancer",
                options=[
                    {"label": "Cáncer de Pulmón", "value": "Pulmón"},
                    {"label": "Cáncer de Mama", "value": "Mama"},
                    {"label": "Cáncer de Colon", "value": "Colon"}
                ],
                value="Pulmón", 
                clearable=False
            )
        ], style={"width": "45%", "display": "inline-block", "marginLeft": "5%"})
    ]),

    dcc.Graph(id="linea-temporal"),


    #5 parte mapa coroplético
    html.H2("5. Mapa coroplético con tasa de mortalidad por departamento"),
    html.P("Este mapa muestra la distribución espacial de la mortalidad por cáncer en Colombia. "
           "El usuario puede seleccionar el año y el tipo de cáncer (Pulmón, Mama o Colon) para observar cómo varía la mortalidad "
           "entre departamentos."),

    html.Div([
        html.Div([
            html.Label("Selecciona año:"),
            dcc.Dropdown(
                id="map-year-dropdown",
                options=[{"label": y, "value": y} for y in years],
                value="2019",  
                clearable=False,
                style={"width": "200px"}
            )
        ], style={"display": "inline-block", "marginRight": "20px"}),

        html.Div([
            html.Label("Selecciona tipo de cáncer:"),
            dcc.Dropdown(
                id="map-cancer-dropdown",   
                options=[
                    {"label": "Pulmón", "value": "Pulmón"},
                    {"label": "Mama", "value": "Mama"},
                    {"label": "Colon", "value": "Colon"}
                ],
                value="Pulmón",   
                clearable=False,
                style={"width": "200px"}
            )
        ], style={"display": "inline-block"})
    ]),

    dcc.Graph(id="choropleth-map"),

    html.H2("Análisis e Interpretación de Resultados", style={"textAlign": "center"}),

    html.H3("Desigualdades Territoriales Identificadas"),
    html.Ul([
        html.Li([
            html.Strong("Norte–Sur y Centro–Periferia: "),
            "Las regiones andinas (Antioquia, Bogotá, Valle) presentan tasas de mortalidad hasta cinco veces superiores frente a las regiones amazónicas y de frontera."
        ]),
        html.Li([
            html.Strong("Brecha Urbano–Rural: "),
            "Las capitales y áreas metropolitanas registran valores significativamente más altos, mientras que en zonas rurales y remotas las tasas son menores, posiblemente por subregistro."
        ]),
        html.Li([
            html.Strong("Desarrollo regional y reporte: "),
            "Departamentos con mayor infraestructura sanitaria muestran tasas más elevadas por mejores capacidades diagnósticas, mientras que en territorios con menor acceso se observan cifras bajas que pueden reflejar subdiagnóstico."
        ]),
    ]),

    html.H3("Factores Explicativos"),
    html.Ul([
        html.Li([
            html.Strong("Sociodemográficos: "),
            "Mayor nivel socioeconómico y urbanización influyen en el acceso al diagnóstico y en el riesgo asociado a estilos de vida urbanos (contaminación, estrés, hábitos)."
        ]),
        html.Li([
            html.Strong("Acceso y calidad en salud: "),
            "Disponibilidad de pruebas diagnósticas, calidad del servicio (oncólogos, equipos, medicamentos), y educación en salud que permite acortar el tiempo entre síntomas, diagnóstico y tratamiento."
        ])
    ]),

    html.H3("Relevancia de la Georreferenciación"),
    html.Ul([
        html.Li("Visibilizar desigualdades territoriales."),
        html.Li("Priorizar intervenciones en zonas críticas."),
        html.Li("Detectar patrones epidemiológicos y clusters regionales."),
        html.Li("Apoyar la planificación de políticas públicas para asignar recursos y evaluar impacto de programas regionales."),
    ])
],style={"fontFamily": "Arial, Helvetica, sans-serif"})


@app.callback(
    [dash.dependencies.Output("graph-bar-can", "figure"),
     dash.dependencies.Output("graph-bar-loc", "figure"),
     dash.dependencies.Output("linea-temporal", "figure"),
     dash.dependencies.Output("choropleth-map", "figure")],
    [dash.dependencies.Input("year-dropdown-can", "value"),
     dash.dependencies.Input("year-dropdown-loc", "value"),
     dash.dependencies.Input("dropdown-depto", "value"),
     dash.dependencies.Input("dropdown-cancer", "value"),
     dash.dependencies.Input("map-year-dropdown", "value"),
     dash.dependencies.Input("map-cancer-dropdown", "value")]   
)
def update_all_graphs(year_can, year_loc, depto, cancer, map_year, map_cancer):
    # --- gráficos de barras ---
    fig_can = px.bar(df, x="tipo_de_cancer", y=year_can,
                     title=f"Tasa de mortalidad por tipo de cáncer ({year_can})",
                     hover_data=["localizacion"])
    
    fig_loc = px.bar(df, x="localizacion", y=year_loc,
                     title=f"Tasa de mortalidad por departamento ({year_loc})",
                     hover_data=["tipo_de_cancer"])
    
    # --- gráfico de línea temporal ---
    df_filtered = df_long[
        (df_long["localizacion"] == depto) & 
        (df_long["tipo_de_cancer"] == cancer)
    ]
    fig_line = px.line(df_filtered, x="Año", y="tasa_mortalidad",
                       title=f"Evolución temporal - {cancer} en {depto}",
                       markers=True)
    fig_line.update_layout(xaxis_title="Año", yaxis_title="Tasa de mortalidad")
    
    # --- mapa coroplético ---
    if map_year and map_year in df.columns:
        df_map_filtered = df[df["tipo_de_cancer"] == map_cancer]

        mapa_with_data = mapa_col.merge(
            df_map_filtered[["DPTO_CCDGO", map_year]],
            on="DPTO_CCDGO", how="left"
        )

        fig_map = px.choropleth(
            mapa_with_data,
            geojson=mapa_with_data.__geo_interface__,
            locations="DPTO_CCDGO",
            featureidkey="properties.DPTO_CCDGO",
            color=map_year,
            hover_name="DPTO_CNMBR",
            title=f"Mapa de mortalidad por {map_cancer} ({map_year})",
            color_continuous_scale="YlOrRd",
            range_color=[0, mapa_with_data[map_year].max()]
        )

        fig_map.update_geos(fitbounds="locations", visible=False)

    else:
        fig_map = px.choropleth(
            mapa_col,
            geojson=mapa_col.__geo_interface__,
            locations="DPTO_CCDGO",
            featureidkey="properties.DPTO_CCDGO",
            color_discrete_sequence=["lightgray"],
            title="Selecciona un año válido para el mapa"
        )
        fig_map.update_geos(fitbounds="locations", visible=False)

    return fig_can, fig_loc, fig_line, fig_map



#Ejecutar la app en local-----------------------------
if __name__ == "__main__":
    app.run(debug=True)
