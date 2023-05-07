# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from dash_svg import Svg, G, Path, Circle
import dash_draggable
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from whitenoise import WhiteNoise

print('--- Restart ---')

parent_path = '' #'/home/imtambovtcev/mysite/'

pio.templates.default = "plotly_white"

df_pictures = pd.read_csv(parent_path+'static/data/diagram_main.csv')
df_pictures.index = df_pictures.id

x0 = df_pictures.position_x.min()-0.5
y0 = df_pictures.position_y.max()+0.5

df_CI = pd.read_csv(parent_path+'static/data/CI_main.csv')
df_CI_x = pd.read_csv(parent_path+'static/data/CI_x_main.csv')
df_CI_x_points = pd.read_csv(parent_path+'static/data/CI_x_points_main.csv')

df_H_H = pd.read_csv(parent_path+'static/data/rotor_H_to_stator_H_main.csv')
df_H_N = pd.read_csv(parent_path+'static/data/rotor_H_to_stator_N_main.csv')
df_H_stator = pd.read_csv(parent_path+'static/data/rotor_H_to_stator_main.csv')
df_tail_H = pd.read_csv(parent_path+'static/data/rotor_tail_to_stator_H_main.csv')
df_tail_N = pd.read_csv(parent_path+'static/data/rotor_tail_to_stator_N_main.csv')
df_tail_stator = pd.read_csv(parent_path+'static/data/rotor_tail_to_stator_main.csv')

data_dihedral = [pd.read_csv(
    parent_path+f'static/data/dihedras_main_{i}.csv') for i in range(4)]

color_pallete = px.colors.qualitative.Alphabet
print(color_pallete)
mode_selected = 'NEB-CI'
molecules_selected = [df_pictures.index[0]]


def html_curve(x_from, x_to, y_from, y_to, x0, y0, name_from, name_to):
    dx = x_to-x_from
    dy = y_to-y_from
    dx = dx if abs(dx) > 0.03 else 0.03
    dy = dy if abs(dy) > 0.03 else 0.03
    # print(f'{dx =} {dy = }')
    if dy > 1:
        dy -= 1
        # print(f'{dx =}')
        if dx < 0:
            dx = abs(dx)
            return html.Div(children=[
                Svg([
                    Path(d=f"M 0 0 C 0 {int(0.5*100*dy)}, {int(120*dx)} {int(0.5*120*dy)}, {int(120*dx)} {int(120*abs(dy))}", stroke='red', fill="transparent")],
                    style={"width": f"{int(120*dx)}px",
                           "height": f"{int(120*dy)}px"}
                    )],
                id=f'{int(name_from)}_{int(name_to)}',
                style={"width": f"{int(120*dx)}px", "height": f"{int(120*abs(dy))}px", "position": "absolute", "top": f"{int(120*(y0-y_to+1))}px", "left": f"{int(120*(x_to-x0)+50)}px"})
        else:
            dx = abs(dx)
            return html.Div(children=[
                Svg([
                    Path(d=f"M 0 {int(120*abs(dy))} C 0 {int(0.5*100*dy)}, {int(120*dx)} {int(0.5*120*dy)}, {int(120*dx)} 0", stroke='red', fill="transparent")],
                    style={"width": f"{int(120*dx)}px",
                           "height": f"{int(120*dy)}px"}
                    )],
                id=f'{int(name_from)}_{int(name_to)}',
                style={"width": f"{int(120*dx)}px", "height": f"{int(120*dy)}px", "position": "absolute", "top": f"{int(120*(y0-y_to+1))}px", "left": f"{int(120*(x_from-x0)+50)}px"})

    elif dy < -1:
        dy = abs(dy)
        dy -= 1
        if dx < 0:
            # print(f'{int(name_from)}_{int(name_to)}')
            dx = abs(dx)
            return html.Div(children=[
                Svg([
                    Path(d=f"M {int(120*dx)} 0 C {int(120*dx)} {int(0.5*120*dy)}, 0 {int(0.5*120*dy)}, 0 {int(120*abs(dy))}", stroke='blue', fill="transparent")],
                    style={"width": f"{int(120*dx)}px",
                           "height": f"{int(120*dy)}px"}
                    )],
                id=f'{int(name_from)}_{int(name_to)}',
                style={"width": f"{int(120*dx)}px", "height": f"{int(120*dy)}px", "position": "absolute", "top": f"{int(120*(y0-y_from+1))}px", "left": f"{int(120*(x_to-x0)+50)}px"})

        else:
            return html.Div(children=[
                Svg([
                    Path(d=f"M 0 0 C 0 {int(0.5*120*dy)}, {int(120*dx)} {int(0.5*120*dy)}, {int(120*dx)} {int(120*abs(dy))}", stroke='blue', fill="transparent")],
                    style={"width": f"{int(120*dx)}px",
                           "height": f"{int(120*dy)}px"}
                    )],
                id=f'{int(name_from)}_{int(name_to)}',
                style={"width": f"{int(120*dx)}px", "height": f"{int(120*dy)}px", "position": " absolute", "top": f"{int(120*(y0-y_from+1))}px", "left": f"{int(120*(x_from-x0)+50)}px"})

    else:
        if dx < -0.83:
            dx = abs(dx)
            dx -= 0.83
            if dy > 0:
                return html.Div(children=[
                    Svg([
                        Path(d=f"M {int(120*dx)} {int(120*abs(dy))} C {int(0.5*120*dx)} {int(120*abs(dy))}, {int(0.5*120*dx)} 0, 0 0", stroke='black', fill="transparent")],
                        style={"width": f"{int(120*dx)}px",
                               "height": f"{int(120*dy)}px"}
                        )],
                    id=f'{int(name_from)}_{int(name_to)}',
                    style={"width": f"{int(120*dx)}px", "height": f"{int(120*dy)}px", "position": "absolute", "top": f"{int(120*(y0-y_to)+60)}px", "left": f"{int(120*(x_to-x0)+100)}px"})
            else:
                dy = abs(dy)
                return html.Div(children=[
                    Svg([
                        Path(d=f"M {int(120*dx)} 0 C {int(0.5*120*dx)} 0, {int(0.5*120*dx)} {int(120*dy)}, 0 {int(120*abs(dy))}", stroke='black', fill="transparent")],
                        style={"width": f"{int(120*dx)}px",
                               "height": f"{int(120*dy)}px"}
                        )],
                    id=f'{int(name_from)}_{int(name_to)}',
                    style={"width": f"{int(120*dx)}px", "height": f"{int(120*dy)}px", "position": "absolute", "top": f"{int(120*(y0-y_from)+60)}px", "left": f"{int(120*(x_to-x0)+100)}px"})
        elif dx > 0.83:
            dx -= 0.83
            if dy > 0:
                return html.Div(children=[
                    Svg([
                        Path(d=f"M {int(120*dx)} 0 C {int(0.5*120*dx)} 0, {int(0.5*120*dx)} {int(120*dy)}, 0 {int(120*abs(dy))}", stroke='black', fill="transparent")],
                        style={"width": f"{int(120*dx)}px",
                               "height": f"{int(120*dy)}px"}
                        )],
                    id=f'{int(name_from)}_{int(name_to)}',
                    style={"width": f"{int(120*dx)}px", "height": f"{int(120*dy)}px", "position": "absolute", "top": f"{int(120*(y0-y_to)+60)}px", "left": f"{int(120*(x_from-x0)+100)}px"})
            else:
                dy = abs(dy)
                return html.Div(children=[
                    Svg([
                        Path(d=f"M 0 0 C {int(0.5*120*dx)} 0, {int(0.5*120*dx)} {int(120*dy)}, {int(120*dx)} {int(120*abs(dy))}", stroke='black', fill="transparent")],
                        style={"width": f"{int(120*dx)}px",
                               "height": f"{int(120*dy)}px"}
                        )],
                    id=f'{int(name_from)}_{int(name_to)}',
                    style={"width": f"{int(120*dx)}px", "height": f"{int(120*dy)}px", "position": "absolute", "top": f"{int(120*(y0-y_from)+60)}px", "left": f"{int(120*(x_from-x0)+100)}px"})

        else:
            print(f'Warninig {int(name_from)}_{int(name_to)}')


def plot_diagram():
    page_width_px = int(120*(df_pictures.position_x.max() -
                        df_pictures.position_x.min()))+100+120
    page_height_px = int(
        120*(df_pictures.position_y.max()-df_pictures.position_y.min()))+120+120
# style={"width": f'{page_width_px}px', 'height': f'{page_height_px}px'},
    return html.Div(id='diagram',  children=[
        html.Div(id=f'{index}_border',
                 children=html.Img(id=f'{index}',
                                   src='data/pics/{}.png'.format(index),
                                   style=({"width": "100px", "height": "120px", "border": f"2px {color_pallete[index%len(color_pallete)]} solid"} if index in molecules_selected else {
                                       "width": "100px", "height": "120px"}),
                                   n_clicks=int(index in molecules_selected)),
                 style={"width": "100px", "height": "120px", "position": "absolute",
                        "top": f"{int(120*(y0-row.position_y))}px", "left": f"{int(120*(row.position_x-x0))}px"}
                 ) for index, row in df_pictures.iterrows()
    ]+[html_curve(df_pictures.loc[int(row.group)].position_x, row.position_x,
                  df_pictures.loc[int(row.group)].position_y, row.position_y, x0, y0, row.group, row.id)
       for index, row in df_pictures.iterrows() if row.group != row.id
       ])


app = Dash(__name__)
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root=parent_path+'static/')

#
# html.Div(className='plot_div', style={"width": "25%", "height": "30%", 'position': 'fixed', "top": '0', 'right': '0'}, children=[
#                 dcc.Graph(figure={}, id='plots')]),

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# App layout
app.layout = html.Div([
    html.Div(children=[plot_diagram(),
                       html.Div(children=[dash_draggable.ResponsiveGridLayout(
                           id='draggable',
                           layouts={
                               "lg": [{
                                   "i": "a",
                                   "x": 12, "y": 0, "w": 5, "h": 13, "static": False
                               }],
                               # "sm": [{
                               #     "i": "a",
                               #     "x":0, "y":0, "w":6, "h":12, "static": True
                               # }
                               # ]
                           },
                           children=[
                               html.Div(id='a', children=[
                                   dcc.Dropdown(['NEB-CI', 'Distance H-H', 'Distance H-N', 'Distance H-stator', 'Distance tail-H', 'Distance tail-N', 'Distance tail-stator', 'dihedral-0', 'dihedral-1',
                                                 'dihedral-2', 'dihedral-3'], 'NEB-CI', id='mode-dropdown'),
                                   dcc.Graph(figure={}, id='plots', responsive=True, style={
                                       # "min-height":"0",
                                       # "flex-grow":"1"
                                   })
                               ])
                           ], style={"isBounded": False, "height": 0}, isBounded=False, resizeHandles=['se']),  # style={"isBounded":True, 'allowOverlap':False, 'preventCollision':True},,  preventCollision=False, isDroppable=True "display":"flex","flex-direction":"column", "flex-grow":"1"

                       ], style={'position': 'fixed', "height": 0, 'width': '100%'})
                       ])
])


# html.Div(
#     style={'width': '35vw', 'display': 'inline-flex', 'position': 'fixed'},
#     children=dash_draggable(
#         id='draggable',
#         axis="both",
#         handle=".handle",
#         defaultPosition={'x': 0, 'y': -1550},
#         position=None,
#         grid=[12, 12],
#         children=[
# dcc.Dropdown(['NEB-CI', 'dihedral-0', 'dihedral-1', 'dihedral-2', 'dihedral-3'], 'NEB-CI', id='mode-dropdown'),
# html.Div(
#     id='a-div',
#     className='handle',
#     children=dcc.Graph(figure={}, id='plots', style={
#                        'width': '35vw', 'zindex': '2147483647', "border": "1px #D3D3D3 solid"})
#             ),

#         ]
#     )),

def update_plot():
    fig = go.Figure()
    if mode_selected is None:
        pass
    elif mode_selected == 'NEB-CI':
        for index in molecules_selected:
            print(f'{index = }')
            fig.add_scatter(x=df_CI_x[f'{index}'].values,y=df_CI[f'{index}'].values, name=f'{index}', line=dict(
                color=color_pallete[index % len(color_pallete)]))

        fig.update_xaxes(range=(0, 1))
        fig.update_layout(
            title="NEB-CI B3LYP/6-31G (d)",
            # xaxis_title="X Axis Title",
            yaxis_title="Energy, eV",
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Cis', 'Trans']
            )
            # legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )
    elif mode_selected == 'Distance H-H':
        for index in molecules_selected:
            print(f'{index = }')
            fig.add_scatter(x=df_CI_x_points[f'{index}'].values,y=df_H_H[f'{index}'].values, name=f'{index}', line=dict(
                color=color_pallete[index % len(color_pallete)]))

        fig.update_xaxes(range=(0, 1))
        fig.update_layout(
            title=mode_selected,
            # xaxis_title="X Axis Title",
            yaxis_title=r'Distance, $\AA$',
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Cis', 'Trans']
            )
            # legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )

    elif mode_selected == 'Distance H-N':
        for index in molecules_selected:
            print(f'{index = }')
            fig.add_scatter(x=df_CI_x_points[f'{index}'].values,y=df_H_N[f'{index}'].values, name=f'{index}', line=dict(
                color=color_pallete[index % len(color_pallete)]))

        fig.update_xaxes(range=(0, 1))
        fig.update_layout(
            title=mode_selected,
            # xaxis_title="X Axis Title",
            yaxis_title=r'Distance, $\AA$',
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Cis', 'Trans']
            )
            # legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )

    elif mode_selected == 'Distance H-stator':
        for index in molecules_selected:
            print(f'{index = }')
            fig.add_scatter(x=df_CI_x_points[f'{index}'].values,y=df_H_stator[f'{index}'].values, name=f'{index}', line=dict(
                color=color_pallete[index % len(color_pallete)]))

        fig.update_xaxes(range=(0, 1))
        fig.update_layout(
            title=mode_selected,
            # xaxis_title="X Axis Title",
            yaxis_title=r'Distance, $\AA$',
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Cis', 'Trans']
            )
            # legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )

    elif mode_selected == 'Distance tail-H':
        for index in molecules_selected:
            print(f'{index = }')
            fig.add_scatter(x=df_CI_x_points[f'{index}'].values,y=df_tail_H[f'{index}'].values, name=f'{index}', line=dict(
                color=color_pallete[index % len(color_pallete)]))

        fig.update_xaxes(range=(0, 1))
        fig.update_layout(
            title=mode_selected,
            # xaxis_title="X Axis Title",
            yaxis_title=r'Distance, $\AA$',
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Cis', 'Trans']
            )
            # legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )

    elif mode_selected == 'Distance tail-N':
        for index in molecules_selected:
            print(f'{index = }')
            fig.add_scatter(x=df_CI_x_points[f'{index}'].values,y=df_tail_N[f'{index}'].values, name=f'{index}', line=dict(
                color=color_pallete[index % len(color_pallete)]))

        fig.update_xaxes(range=(0, 1))
        fig.update_layout(
            title=mode_selected,
            # xaxis_title="X Axis Title",
            yaxis_title=r'Distance, $\AA$',
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Cis', 'Trans']
            )
            # legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )

    elif mode_selected == 'Distance tail-stator':
        for index in molecules_selected:
            print(f'{index = }')
            fig.add_scatter(y=df_tail_stator[f'{index}'].values, name=f'{index}', line=dict(
                color=color_pallete[index % len(color_pallete)]))

        fig.update_xaxes(x=df_CI_x_points[f'{index}'].values,range=(0, 1))
        fig.update_layout(
            title=mode_selected,
            # xaxis_title="X Axis Title",
            yaxis_title=r'Distance, $\AA$',
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Cis', 'Trans']
            )
            # legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )

    elif 'dihedral' in mode_selected:
        _df = data_dihedral[int(mode_selected[-1])]
        for index in molecules_selected:
            print(f'{index = }')
            fig.add_scatter(x=df_CI_x_points[f'{index}'].values,y=_df[f'{index}'].values, name=f'{index}', line=dict(
                color=color_pallete[index % len(color_pallete)]))

        fig.update_xaxes(range=(0, 1))
        fig.update_layout(
            title=mode_selected,
            # xaxis_title="X Axis Title",
            yaxis_title=r'$Angle, ^\circ$',
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1],
                ticktext=['Cis', 'Trans']
            )
            # legend_title="Legend Title",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="RebeccaPurple"
            # )
        )
    # fig.update_layout(transition_duration=300)
    return fig


@ callback(
    Output(component_id='plots', component_property='figure'),
    *[Output(component_id=f'{i}', component_property='style')
      for i in df_pictures.index],
    Input('mode-dropdown', 'value'),
    *[Input(component_id=f'{i}', component_property='n_clicks') for i in df_pictures.index]
)
def update_graph(*args):
    global mode_selected
    global molecules_selected
    print(args)
    mode_selected = args[0]
    print(f'{mode_selected = }')
    molecules_selected = [index for i, index in zip(
        args[1:], df_pictures.index) if i % 2]
    print(f'{molecules_selected = }')
    # fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return update_plot(), *[{"width": "100px", "height": "120px", "border": f"2px {color_pallete[i%len(color_pallete)]} solid"} if i in molecules_selected else {"width": "100px", "height": "120px"} for i in df_pictures.index]


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
