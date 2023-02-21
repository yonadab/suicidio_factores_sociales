# -*- coding: utf-8 -*-
"""

@author: Yonadab Jared Guzmán Mendoza

"""

###################################################################
#                                                                 #
# - Suicidios: Muertes totales por suicidio independiente del     #
#              método o la edad                                   #
#                                                                 #
# - Inseguridad: Porcentaje de percepción de inseguridad de la    #
#                población                                        #
#                                                                 #
# - Víctima_delitos: Cantidad de víctimas registradas en los      #
#                    órganos jurisdiccionales de primera ins-     #
#                    tancia                                       #
#                                                                 #
###################################################################

#-----------------------------------------------------------------#
#                                                                 #
# Links:                                                          #
#                                                                 #
#  https://www.inegi.org.mx/programas/cnije/2016/#Tabulados       #
#  https://www.inegi.org.mx/temas/salud/                          #
#  https://www.inegi.org.mx/temas/percepcion/                     #
#                                                                 #
#-----------------------------------------------------------------#

import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go



df = pd.read_csv('./Suicidio_inseguridad.csv', encoding='latin1')

df = df.astype({'Año':'str'})

#### STREAMLITE ####

st.set_page_config(page_title='Factores psicosociales',
                   page_icon=':chart_with_upwards_trend:',
                   layout='wide')



#### SIDEBAR ####

st.sidebar.header('Selecciona para filtrar :mag_right:')

entidad = st.sidebar.multiselect(
    'Selecciona la Entidad:',
    options=df['Entidad'].unique(),
    default=df['Entidad'].unique())


year = st.sidebar.multiselect(
    'Selecciona el año:',
    options=df['Año'].unique(),
    default=df['Año'].unique())

df_selection = df.query('Entidad == @entidad & Año == @year')

#st.dataframe(df_selection)


#---- MAIN PAGE ----#

st.title('Suicidio y factores de riesgo :red_circle:')
st.caption('by: Yonadab Jared Guzmán Mendoza')


with st.expander('Información sobre los datos'):
    st.write('Los datos fueron recopilados desde la página oficial del INEGI. Posteriormente fueron procesados\
             para su correcta visualización.')
             
    st.write('**-Suicidios:** Muertes por suicidio independiente del método utilizado')
    st.write('**-Inseguridad:** Porcentaje sobre la percepción de inseguridad de la población')
    st.write('**-Victimización:** Cantidad de víctimas registradas en los órganos jurisdiccionales de primera instancia')
    st.write('**ANEXO DE LAS FUENTES DE INEGI**')
    st.write('https://www.inegi.org.mx/programas/cnije/2016/#Tabulados')
    st.write('https://www.inegi.org.mx/temas/salud/')
    st.write('https://www.inegi.org.mx/temas/percepcion/')
    st.write('_Date una vuelta por mi Github_ :smile:')
    st.write('https://github.com/yonadab')
        




st.markdown("---")



########## CREAMOS LAS TABLAS #############

tab1, tab2, tab3, tab4 = st.tabs(['Suicidios','Inseguridad',"KPI's", 'Datos'])



with tab1:
    

    
      
    import json

    with open('mexicoHigh.json', 'r', encoding='utf-8') as f:
        coordenadas = json.load(f)
            
    suicidios = df_selection.groupby('Entidad').sum()
        
    mapa = px.choropleth(data_frame=suicidios,
                         geojson=coordenadas,
                         locations=suicidios.index,
                         featureidkey='properties.name',
                         color=suicidios['Suicidios'],
                         color_continuous_scale="purples",
                         title='Número de suicidios cometidos por estado')
        
    mapa.update_geos(fitbounds="locations", visible=False)
    mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
    st.plotly_chart(mapa, use_container_width=True)

    st.markdown('---')

    
    #--- GRAFICO PRINCIPAL SUICIDIO ---#
    group_entidad = df_selection.groupby(by='Entidad').sum()
        
    group_media = df_selection.groupby(by='Entidad').agg({'Suicidios':'mean'})
        
    fig = px.bar(group_entidad, 
                     x=group_entidad.index,
                     y=group_entidad['Suicidios'])
        
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    
    #-- BOTÓN PARA CALCULAR LA MEDIA --#
    media = st.checkbox('Calcular la media de suicidios')
    
    if media:
    
        group_media = df_selection.groupby(by='Entidad').agg({'Suicidios':'mean'})
    
        indx = group_media.index
    
        fig.add_scatter(x=indx,
                        y=group_media['Suicidios'],
                        mode = 'lines+markers',
                        marker=dict(color='#BE00FA', size=5),
                        name='Media de suicidios')
    
    
    ### GRAFICAMOS ###
    st.plotly_chart(fig, markers=True, use_container_width=True)
    





with tab2:
    
    inseguridad_anual = df_selection.groupby('Año').mean()
    
    
    diferencia_anual = st.checkbox('Ver diferenciación anual')
    
    
    if diferencia_anual:
    ##-- OBTENER LA DIFERENCIA EN % ANUAL --##
        inseg = inseguridad_anual['Inseguridad']
        anual_2017,anual_2018, anual_2019, anual_2020, anual_2021 = inseg.iloc[0], inseg.iloc[1], inseg.iloc[2], inseg.iloc[3], inseg.iloc[4]
    
        ## Obtener porcentaje: Año final - Año inicial / 100 * 100
        porcentaje_1 = ((anual_2018 - anual_2017) / anual_2017) *100
        porcentaje_2 = ((anual_2019 - anual_2018) / anual_2018) *100
        porcentaje_3 = ((anual_2020 - anual_2019) / anual_2019) *100
        porcentaje_4 = ((anual_2021 - anual_2020) / anual_2020) *100
        
        st.write(f'% de diferencia entre 2017 y 2018:  **{porcentaje_1:.3}**')
        st.write(f'% de diferencia entre 2018 y 2019:  **{porcentaje_2:.3}**')
        st.write(f'% de diferencia entre 2019 y 2020:  **{porcentaje_3:.3}**')
        st.write(f'% de diferencia entre 2020 y 2021:  **{porcentaje_4:.3}**')

    
    
    fig_inseguridad = px.bar(x=inseguridad_anual.index,
                             y=inseguridad_anual['Inseguridad'],
                             title='Media del % de percepción de la inseguridad',
                             color=inseguridad_anual.index,
                             labels=dict(x='Año', y='Inseguridad'))
    

    fig_inseguridad.update_layout(showlegend=False)
    
    
    ## -- MARCAR TENDENCIA --##
    
    tendencia_scatter = st.checkbox('Marcar tendencia')
    
    if tendencia_scatter:
        fig_inseguridad.add_trace(go.Scatter(x=inseguridad_anual.index,
                                    y=inseguridad_anual['Inseguridad'],
                                    line=dict(color='black')))
    
    
    
    st.plotly_chart(fig_inseguridad)
    
    with st.expander('Más información'):
            
        st.write("**La inseguridad se refiere al porcentaje de percepción de inseguridad que tienen los cuidadanos.**")
        st.write('Los datos anuales son presentados calculando el promedio entre los 32 estados de la república para cada año correspondiente.')
        st.write('El pico más alto de percepción sobre inseguridad se da en el año 2018. Sin embargo, en los\
                 en los años consecuentes se puede observar una disminución de la percepción de inseguridad')
        st.write('**_ver diferenciación anual para más detalles_')
                 
    
    
    
    
with tab3:
    
    
    sum_suicidio = df_selection.groupby('Entidad').agg({'Suicidios':'sum'})
    sum_victimas =df_selection.groupby('Entidad').agg({'victimas_delitos':'sum'})
        
    prevalencia_suicidio= sum_suicidio.apply(lambda x: x/1000)
    prevalencia_victimas = sum_victimas.apply(lambda x: x/1000)
        
    tasa_suicidios = prevalencia_suicidio['Suicidios'].values
    tasa_victimas = prevalencia_victimas['victimas_delitos'].values
        
    
       
    fig_bar = px.scatter(x=tasa_suicidios,
                         y=tasa_victimas,
                         title='Tasa de suicidios y victimización por cada mil habitantes',
                         labels=dict(x='Suicidios', y='Victimización'),
                         trendline='ols')
        
    fig_bar.update_traces(marker=dict(color='RoyalBlue'))
                
    st.plotly_chart(fig_bar)
        
    # correlacion pearson
    from scipy import stats
    
    corr = stats.pearsonr(prevalencia_suicidio['Suicidios'],
                          y=prevalencia_victimas['victimas_delitos'])
        
    
    st.write(f'**Coeficiente de Correlacion Pearson:** {corr[0]}')
        
    
    with st.expander('Más información'):
            
        st.write("**Correlación entre la tasa de suicidios vs la tasa de victimización por cada mil habitantes.**\
                   La victimización se refiere a la cantidad de víctimas registradas en los órganos jurisdiccionales\
                  de primera estancia independientemente de su motivo (asalto, robo, violación, etc.).")
                     
        st.write('En términos generales, se puede observar una correlación positiva entre ambas variables; tomar en cuenta\
                 que la correlación dependerá de el año elegido y los estados _(juega con la barra lateral para observar su comportamiento)_')
                     
        st.write('La línea marca la tendencia de los datos y es ajustada mediante los _mínimos cuadrados ordinarios (OLS)_')
    
    st.markdown('---')
    
    
    
    ####------ REGRESION LINEAL -----####
    
    group_df = df_selection.groupby(['Entidad']).sum()
    
    X = group_df['Inseguridad'].values.reshape(-1,1)
    y = group_df['victimas_delitos'].values
    
    model = LinearRegression().fit(X,y)
    
    x_range = np.linspace(X.min(), X.max(), 32)
    y_range = model.predict(x_range.reshape(-1,1))
        
    color_str = group_df['Suicidios'].astype(str)
    
    fig_regression = px.scatter(group_df,
                                x=group_df['Inseguridad'],
                                y=group_df['victimas_delitos'],
                                title='Victimización VS Percepción de inseguridad',
                                color=color_str)
    
    fig_regression.update_layout(showlegend=False)
    fig_regression.add_traces(go.Scatter(x=x_range, y=y_range, name='Ajuste de regression'))
    st.plotly_chart(fig_regression)
    
    with st.expander('Más información'):
            
        st.write("**Regresión lineal sobre percepción de inseguridad vs Victimización**")
        st.write('Se observa la poca interacción entre ambas variables, lo cual nos indica que\
                 no tienen una relación lineal directa entre ambas. La pobre tendencia nos impide\
                 generar una predicción lineal a partir de ambas variables')
    
    
    ###---- PLOT 3D ----###
    
    st.markdown('---')
    
    fig_3d = px.scatter_3d(group_df,
                           x=group_df['Suicidios'],
                           y=group_df['Inseguridad'],
                           z=group_df['victimas_delitos'],
                           color=color_str,
                           color_discrete_sequence=['red','blue','gray'],
                           title='Percepción de inseguridad, Victimización y Suicidios',
                           labels=dict(x='Suicidios', y='Inseguridad', z='Victimizacion'))
    
    fig_3d.update_layout(showlegend=False)
   
    st.write('Utiliza tu cursor :arrow_up: :arrow_down: para hacer zoom')
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    with st.expander('Más información'):
            
        st.write("**Observación de las 3 variables**")
        st.write('Se observan grandes conjuntos en común para las 3 variables, lo cual nos\
                 indica que probablemente se puedan encontrar patrones entre la interacción de\
                las variables utilizando KNN o algún método de clasificación')
    
    
with tab4:
    
    st.write('**Dataframe con los datos crudos**')
    st.caption('Estos datos han sido recopilados y limpiados para su posterior almacenaje. _Click en: Información sobre los datos_ para más información_')
        
    st.dataframe(df_selection)
    
    
    
    
    
###### REMOVIENDO DETALLES FINALES DE STREAMLIT ######

hide_st_style = """
	<style>
	#MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
	header {visibility: hidden;}
	</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)




