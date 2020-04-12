# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:18:05 2020

@author: Carlos
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html

covid="C:/Users/Carlos/Downloads/casos1.csv"
datos=pd.read_csv(covid)
datos.columns=["id","fecha","ciudad","depto","estado","edad","sexo","origen","pais"]
datos.set_index("id",inplace=True)
datos.fecha=pd.to_datetime(datos.fecha, format='%d/%m/%Y')
datos.estado=datos.estado.str.lower()

x_fecha=datos.fecha.value_counts().rename_axis("Fecha").reset_index(name="Casos")
x_depto=datos.depto.value_counts().rename_axis('Departamentos').reset_index(name='Casos')
x_estado=datos.estado.value_counts().rename_axis('Estado').reset_index(name='Casos')
x_edad=datos.edad.value_counts().rename_axis('Edad').reset_index(name='Casos')
x_sexo=datos.sexo.value_counts().rename_axis('sexo').reset_index(name='Casos')


fig_depto=px.scatter(x_depto.head(10),x="Departamentos", 
                   y="Casos", size="Casos",
                   color="Departamentos",title="Casos x Departamento",
                   hover_name="Departamentos",size_max=60,text="Casos")

fig_fecha=px.bar(x_fecha, x="Fecha",y="Casos",
           text="Casos",title="Casos x dia",color_discrete_sequence=["red"])
fig_fecha.update_traces(textposition='outside')
fig_fecha.add_annotation(x=x_fecha.loc[25][0],y=10,xref="x",yref="y",text="Daño en la maquina",showarrow=True,
                         font=dict(family="Courier New, monospace",size=16,color="white"),
                         align="center",arrowhead=1,arrowsize=1,arrowwidth=2,arrowcolor="yellow",ax=0,ay=-200,
                         bordercolor="black",borderwidth=1,borderpad=4,bgcolor="navy",opacity=1)


fig_estado= go.Figure(go.Pie(
    values = x_estado.Casos,
    labels = x_estado.Estado.str.capitalize(),
    texttemplate = "%{label}: %{value:} <br>(%{percent})",
    textposition = "auto"))

bins=[0,10,20,30,40,50,60,70,80,90,100]
rango_edad=["0 a 10","11 a 20","21 a 30",
         "31 a 40","41 a 50","51 a 60",
         "61 a 70","71 a 80","81 a 90","91 a 100"]
datos.edad=pd.cut(datos.edad,bins,labels=rango_edad)  #sirve para agrupar las edaddes en rangos
datos_m=datos[(datos.sexo=="M")] #datos masculino
datos_f=datos[(datos.sexo=="F")]
edad_m=datos_m.edad.value_counts().rename_axis('Edad').reset_index(name='Casos').sort_values('Edad',ascending=False)
edad_f=datos_f.edad.value_counts().rename_axis('Edad').reset_index(name='Casos').sort_values('Edad',ascending=False)

fig_edad = go.Figure(data=[
    go.Bar(name='Masculino',x=edad_m.Casos,y=edad_m.Edad,orientation='h',
          marker=dict(color='cornflowerblue',line=dict(color="black", width=3))),
    go.Bar(name='Femenino',x=edad_f.Casos,y=edad_f.Edad,orientation='h',
           marker=dict(color='rgba(246, 78, 139, 0.6)',line=dict(color='rgba(0,0,0, 1.0)', width=3))),
])
fig_edad.update_layout(barmode='stack',title="Casos x edad & sexo",yaxis_title="Edades",xaxis_title="Casos",
                      font=dict(family="Courier New, monospace",size=18,color="black"))


server = flask.Flask(__name__)
app=dash.Dash(__name__,server=server)
app.layout=html.Div([
    dcc.Graph(figure=fig_depto),
    dcc.Graph(figure=fig_fecha),
    dcc.Graph(figure=fig_estado),
    dcc.Graph(figure=fig_edad),
    
])
if __name__== "__main__":
    app.run_server(debug=True, use_reloader=False)


