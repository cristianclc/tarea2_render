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
mapa_col = gpd.read_file("COLOMBIA/COLOMBIA.shp", encoding='latin1')

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
    
    # --- TÍTULO PRINCIPAL ---
    html.H1("Dashboard de Análisis - Tasa de Mortalidad por Cáncer en Colombia", 
            style={"textAlign": "center", "marginBottom": "40px"}),

    html.Div([
        html.H2("1. Introducción y Objetivo del Análisis", 
                style={"color": "#2c3e50", "borderBottom": "2px solid #2c3e50", "paddingBottom": "10px"}),

        html.P("Este dashboard tiene como propósito analizar la evolución y distribución territorial "
               "de la tasa de mortalidad por distintos tipos de cáncer en Colombia entre los años 1997 y 2019. "
               "Permite identificar patrones temporales y regionales relevantes para la salud pública."),

        html.H3("Fuente de datos"),
        html.P([
            html.Strong("Fuente: "),
            "Departamento Administrativo Nacional de Estadística (DANE) e Instituto Nacional de Cancerología"
        ]),
        html.P([
            html.Strong("Enlace al dataset: "),
            html.A("Tasa de mortalidad por tipo de cáncer (Datos Abiertos Colombia)",
                   href="https://www.datos.gov.co/Salud-y-Protecci-n-Social/Tasa-de-mortalidad-por-tipo-de-c-ncer/64it-izw2/about_data",
                   target="_blank")
        ]),

        html.H3("Variables principales"),
        html.Ul([
            html.Li("Localización: Departamento o región de análisis."),
            html.Li("Tipo de cáncer: Categoría del cáncer (Pulmón, Mama, Colon, etc.)."),
            html.Li("Tasa de mortalidad: Número de muertes por cada 100,000 habitantes por año."),
        ]),
    ], style={"backgroundColor": "#ffffff", "padding": "25px", "borderRadius": "10px",
              "boxShadow": "0px 2px 5px rgba(0,0,0,0.1)", "marginBottom": "40px"}),

    html.Div([
        html.H2("2. Visualizaciones y Exploración de Datos", 
                style={"color": "#2c3e50", "borderBottom": "2px solid #2c3e50", "paddingBottom": "10px"}),

        html.H3("Tasa de mortalidad por departamento"),
        html.P("Comparación de la tasa de mortalidad entre los diferentes departamentos en un año específico."),
        dcc.Dropdown(
            id="year-dropdown-loc",
            options=[{"label": y, "value": y} for y in years],
            value="2000"
        ),
        dcc.Graph(id="graph-bar-loc", style={"marginBottom": "40px"}),

        html.H3("Tasa de mortalidad por tipo de cáncer"),
        html.P("Comparación de mortalidad según el tipo de cáncer en el año seleccionado."),
        dcc.Dropdown(
            id="year-dropdown-can",
            options=[{"label": y, "value": y} for y in years],
            value="2000"
        ),
        dcc.Graph(id="graph-bar-can", style={"marginBottom": "40px"}),

        html.H3("Boxplots comparativos de cánceres frecuentes (Pulmón, Mama, Colon)"),
        html.P("Distribución de tasas de mortalidad en tres de los cánceres más frecuentes en 2000 vs 2018."),
        dcc.Graph(figure=fig_box_pul),
        dcc.Graph(figure=fig_box_mama),
        dcc.Graph(figure=fig_box_colon, style={"marginBottom": "40px"}),

        html.H3("Evolución temporal por departamento y tipo de cáncer"),
        html.P("Tendencia temporal de la mortalidad en un tipo de cáncer y departamento específicos."),
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
            ], style={"width": "45%", "display": "inline-block", "marginLeft": "5%"}),
        ]),
        dcc.Graph(id="linea-temporal", style={"marginBottom": "40px"}),

        html.H3("Mapa coroplético de mortalidad"),
        html.P("Distribución espacial de la tasa de mortalidad por tipo de cáncer y año seleccionado."),
        html.Div([
            html.Div([
                html.Label("Selecciona año:"),
                dcc.Dropdown(
                    id="map-year-dropdown",
                    options=[{"label": y, "value": y} for y in years],
                    value="2019", clearable=False, style={"width": "200px"}
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
                    value="Pulmón", clearable=False, style={"width": "200px"}
                )
            ], style={"display": "inline-block"}),
        ]),
        dcc.Graph(id="choropleth-map"),

    ], style={"backgroundColor": "#ffffff", "padding": "25px", "borderRadius": "10px",
              "boxShadow": "0px 2px 5px rgba(0,0,0,0.1)", "marginBottom": "40px"}),


    html.Div([
    html.H2("3. Conclusiones e Interpretación de Resultados", 
            style={"color": "#2c3e50", "borderBottom": "2px solid #2c3e50", "paddingBottom": "10px"}),

    html.H3("Desigualdades Territoriales Identificadas"),
    html.Ul([
        html.Li("Las regiones andinas —especialmente Antioquia, Bogotá y Valle del Cauca— concentran las tasas de mortalidad por cáncer más elevadas del país. "
                "Estas zonas presentan valores hasta cinco veces superiores frente a departamentos periféricos o amazónicos, lo que refleja tanto una mayor carga de enfermedad como mejores sistemas de registro y diagnóstico.", style={"marginBottom": "10px"}),
        html.Li("Existe una marcada brecha urbano–rural. En las capitales y áreas metropolitanas, la mortalidad es mayor debido a una combinación de factores: "
                "mayor exposición a riesgos ambientales, hábitos de vida urbanos, envejecimiento poblacional y mejor acceso a diagnóstico. "
                "En contraste, en zonas rurales y apartadas, las tasas más bajas pueden estar asociadas a subregistro o falta de acceso a servicios de salud.", style={"marginBottom": "10px"}),
        html.Li("Departamentos con infraestructura sanitaria más desarrollada —como Cundinamarca, Antioquia o Valle— tienden a mostrar tasas más altas. "
                "Esto no necesariamente implica peores condiciones de salud, sino una detección más efectiva de casos, lo cual resalta la importancia del fortalecimiento institucional en la vigilancia epidemiológica.", style={"marginBottom": "10px"}),
    ]),

    html.H3("Factores Explicativos"),
    html.Ul([
        html.Li("Los factores sociodemográficos y económicos juegan un papel clave. Las poblaciones con mayores niveles de urbanización, envejecimiento y consumo de tabaco o alcohol presentan una mayor exposición al riesgo. "
                "A su vez, las condiciones laborales y ambientales, como la contaminación y la exposición a sustancias químicas, agravan la situación en regiones industriales.", style={"marginBottom": "10px"}),
        html.Li("El acceso y la calidad del sistema de salud son determinantes en la mortalidad. "
                "En departamentos con cobertura limitada, diagnósticos tardíos y escasez de personal especializado contribuyen a aumentar las tasas de mortalidad. "
                "Asimismo, las desigualdades en el gasto público en salud generan diferencias en la capacidad de respuesta regional.", style={"marginBottom": "10px"}),
        html.Li("Las políticas de prevención y detección temprana son variables críticas. Programas como campañas de vacunación (por ejemplo, contra el VPH), detección de cáncer de mama o colonoscopías regulares tienen efectos diferenciales según el territorio y la inversión institucional.", style={"marginBottom": "10px"}),
    ]),

    html.H3("Relevancia de la Georreferenciación"),
    html.Ul([
        html.Li("La visualización geográfica de la mortalidad por cáncer permite identificar con claridad patrones territoriales, brechas regionales y zonas críticas que podrían pasar desapercibidas en análisis puramente estadísticos.", style={"marginBottom": "10px"}),
        html.Li("El enfoque espacial facilita la priorización de políticas públicas focalizadas, orientando los recursos hacia departamentos con mayor vulnerabilidad o menor capacidad diagnóstica. "
                "Esto favorece una gestión sanitaria más equitativa y eficiente.", style={"marginBottom": "10px"}),
        html.Li("Además, el análisis georreferenciado permite detectar posibles clusters epidemiológicos, asociar la mortalidad a determinantes sociales del entorno (como pobreza, contaminación o acceso a servicios), y evaluar el impacto de programas regionales de salud.", style={"marginBottom": "10px"}),
        html.Li("En conjunto, la integración de datos epidemiológicos y espaciales fortalece la toma de decisiones en salud pública y permite una planificación más estratégica basada en evidencia territorial.", style={"marginBottom": "10px"}),
    ]),
], 
style={
    "backgroundColor": "#ffffff",
    "padding": "25px",
    "borderRadius": "10px",
    "boxShadow": "0px 2px 5px rgba(0,0,0,0.1)",
    "marginBottom": "40px"
})
,

], style={
    "fontFamily": "Arial, Helvetica, sans-serif",
    "backgroundColor": "#f8f9fa",
    "padding": "40px"
})

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
