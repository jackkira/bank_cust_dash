import pandas as pd
from dash import Dash, Input, dcc, html, Output, dash, State
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv("assets/Bank_customer_dataset.csv")
external_stylesheets = ['https://codepen.io/unicorndy/pen/GRJXrvP.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

alert = dbc.Alert("Please choose Credit Score Type from dropdown to avoid further disappointment!", color="red",
                  dismissable=True),  # use dismissible or duration=5000 for alert to close in x milliseconds

# Overwrite your CSS setting by including style locally
colors = {
    'background': '#2D2D2D',
    'text': '#E1E2E5',
    'figure_text': '#ffffff',
    'confirmed_text': '#3CA4FF',
    'deaths_text': '#f44336',
    'recovered_text': '#5A9E6F',
    'highest_case_bg': '#393939',

}

# Creating custom style for local use
divBorderStyle = {
    'backgroundColor': '#393939',
    'borderRadius': '12px',
    'lineHeight': 0.9,
}

# Creating custom style for local use
boxBorderStyle = {
    'borderColor': '#393939',
    'borderStyle': 'solid',
    'borderRadius': '10px',
    'borderWidth': 2,
}

# total Customer
df_customer_total = df['CustomerId'].count()
df_active_total = len(df[df['IsActiveMember'] == 1])
df_creditcard_total = len(df[df['HasCrCard'] == 1])


# CreditScore Good or Bad
def credit_score_table(row):
    credit_score = row.CreditScore
    if 300 <= credit_score < 500:
        return "Very Poor"
    elif 500 <= credit_score < 601:
        return "Poor"
    elif 601 <= credit_score < 661:
        return "Fair"
    elif 661 <= credit_score < 781:
        return "Good"
    elif credit_score >= 851:
        return "Top"
    elif 781 <= credit_score < 851:
        return "Excellent"
    elif credit_score < 300:
        return "Deep"


df['credit_tag'] = df.apply(credit_score_table, axis=1)

app.layout = html.Div([
    html.Div([
        # Title
        html.Div([
            html.H1(children='Bank Customer Analytics Dummy Data',
                    style={
                        'textAlign': 'left', 'color': colors['text'], 'backgroundColor': colors['background'], },
                    className='ten columns', )], className="row"),
        # Total Customer, Active Members and CreditCard
        html.Div([
            html.Div([
                html.H4(children='Total Customer: ', style={'textAlign': 'center', 'color': "#33c3f0", }),
                html.P(f"{df_customer_total:,d}", style={'textAlign': 'center', 'color': "#33c3f0", 'fontSize': 30, })],
                style=divBorderStyle, className='four columns', ),
            html.Div([
                html.H4(children='Total Active Members: ', style={'textAlign': 'center', 'color': "#33c3f0", }),
                html.P(f"{df_active_total:,d}", style={'textAlign': 'center', 'color': "#33c3f0", 'fontSize': 30, })],
                style=divBorderStyle, className='four columns', ),
            html.Div([
                html.H4(children='Total Creditcard User: ', style={'textAlign': 'center', 'color': "#33c3f0", }),
                html.P(f"{df_creditcard_total:,d}", style={'textAlign': 'center', 'color': "#33c3f0", 'fontSize': 30, })
            ],
                style=divBorderStyle, className='four columns', )
        ]),
        # Male and female Country Vise
        html.Div([
            html.H4(children='Male and Female count by Country',
                    style={
                        'textAlign': 'left',
                        'color': colors['text'],
                        'backgroundColor': colors['background'],

                    },
                    className='twelve columns'
                    ),
            html.Div([
                # Male and female Country Vise
                dcc.Dropdown(id="geo_dropdown",
                             options=df['Geography'].unique(),
                             value='Spain',
                             style={'fontSize': 20,
                                    'color': colors['text']
                                    }, ),
            ], className='twelve columns'),
            html.Div((
                html.Div([
                    dcc.Graph(id='graph')
                ], className='four columns'),
                # Tenure
                html.Div([
                    dcc.Graph(id='tenure_graph')
                ], className='four columns'),
                # Number of Product by GEO and SEX
                html.Div([
                    dcc.Graph(id='num_of_prod_graph')
                ], className='four columns'),
            ), className='twelve columns', style={'margin-bottom': '5rem'}),
            # sum_balance_scatter
            html.Div([
                html.Div([
                    dcc.Graph(id='sum_balance_scatter')
                ], className='twelve columns'),
            ], className='twelve columns', style={'margin-bottom': '5rem'}),
            html.Div([
                dcc.Dropdown(id="sex_dropdown",
                             options=df['Gender'].unique(),
                             value='Male',
                             style={'fontSize': 20,
                                    'color': colors['text']
                                    }, ),
            ], className='twelve columns'),

            html.Div([
                # AGE
                html.Div([
                    dcc.Graph(id='age_graph')
                ], className='six columns'),
                # sum balance by GEO and SEX
                html.Div([
                    dcc.Graph(id='sum_balance_graph')
                ], className='six columns'),
            ], className='twelve columns', style={'margin-bottom': '5rem'}),
            html.Div([
                # CreditScore 5 Level
                html.Div([
                    html.Div([
                        html.Div(id="credit_alert", children=[]),
                        dcc.Dropdown(id="credit_dropdown",
                                     options=df['credit_tag'].unique(),
                                     value=['Good', 'Poor'],
                                     style={'fontSize': 18,
                                            'color': 'black'
                                            },
                                     multi=True, persistence=True, persistence_type='session'),
                    ], className='twelve columns', style={'margin-bottom': '0.5rem'}),
                    html.Div([
                        html.Button(id='my-button', n_clicks=0, children="Show breakdown", style={'text': 'white',
                                                                                                  'color': 'white'},)
                    ]),
                    html.Div([
                        dcc.Graph(id='credit_graph', figure={})
                    ], className='twelve columns'),
                ], className='twelve columns'),
            ], className='nine columns, offset-by-two columns'),
        ], className="row"),
    ], className="row"),
])


# for Gender by Geography
@app.callback(
    Output("graph", "figure"),
    Input("geo_dropdown", "value"), )
def update_bar_chart(geo):
    mask_geo = df["Geography"] == geo
    fig = px.pie(df[mask_geo], names='Gender',
                 title=f'Gender count of {geo}',
                 color_discrete_sequence=px.colors.qualitative.T10,
                 hole=0.6)
    fig.update_layout(
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0, r=0, t=65, b=0),
        height=350,
    )
    return fig


# sum_balance_scatter
@app.callback(
    Output("sum_balance_scatter", "figure"),
    Input("geo_dropdown", "value"),)
def update_bar_chart(geo):
    df['Exited'] = df['Exited'].astype(str)
    mask_geo = df["Geography"] == geo
    fig = px.scatter(df[mask_geo], y='Age', x='CreditScore', size='Balance',
                     symbol='Exited', color='Exited', title=f'Exited Scatter Plot with AGE and Balance of {geo}',
                     color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_traces(marker=dict(line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))

    fig.update_layout(
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0, r=0, t=65, b=0),
        height=350,
    )
    return fig


# for Gender by CreditScore 5 Level
@app.callback([
    Output('credit_graph', 'figure'),
    Output('credit_alert', 'children')],
    [Input('my-button', 'n_clicks')],
    [State('credit_dropdown', 'value')]
)
def update_credit_tag(n, selected_credit_type):
    if len(selected_credit_type) == 0:
        return dash.no_update, alert
    else:
        mask_cred = df[df["credit_tag"].isin(selected_credit_type)]
        fig = px.histogram(mask_cred, x='credit_tag', color='Exited', barmode='group',
                           color_discrete_sequence=px.colors.qualitative.T10)
        fig.update_layout(hovermode='x', font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
                          legend=dict(
                              traceorder="normal",
                              font=dict(
                                  family="sans-serif",
                                  size=12,
                                  color=colors['figure_text']
                              ),
                              bgcolor=colors['background'],
                              borderwidth=5
                          ),
                          paper_bgcolor=colors['background'],
                          plot_bgcolor=colors['background'],
                          margin=dict(l=0, r=0, t=65, b=0),
                          height=350,
                          )

        return fig, dash.no_update


# AGE
@app.callback(
    Output('age_graph', 'figure'),
    Input('sex_dropdown', 'value')
)
def update_age_chart(selected_sex_type):
    mask_cred = df["Gender"] == selected_sex_type
    fig = px.histogram(df[mask_cred], x='Age', nbins=10, text_auto=True,
                       title=f'AGE count of {selected_sex_type}',
                       color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_layout(
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0, r=0, t=65, b=0),
        height=350,
        bargap=0.1,
    )
    return fig


# Tenure
@app.callback(
    Output("tenure_graph", "figure"),
    Input("geo_dropdown", "value"))
def update_bar_chart(geo):
    mask_geo = df["Geography"] == geo
    fig = px.histogram(df[mask_geo], x='Tenure', text_auto=True, title=f"Tenure of {geo}",
                       color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_layout(
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0, r=0, t=65, b=0),
        height=350,
        bargap=0.1,
    )
    return fig


# sum_balance
@app.callback(
    Output('sum_balance_graph', 'figure'),
    Input('sex_dropdown', 'value')
)
def update_sum_balance_chart(selected_sum_balance_type):
    mask_cred = df['Gender'] == selected_sum_balance_type
    fig = px.histogram(df[mask_cred], x='Geography', y='Balance', text_auto=True,
                       title=f'Summation Balance of {selected_sum_balance_type}',
                       color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_layout(
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0, r=0, t=65, b=0),
        height=350,
        bargap=0.1,
    )
    return fig


# Number of Product
@app.callback(
    Output("num_of_prod_graph", "figure"),
    Input("geo_dropdown", "value"))
def update_nop_chart(geo):
    mask_geo = df["Geography"] == geo
    fig = px.histogram(df[mask_geo], x='NumOfProducts', color='Gender', barmode='group',
                       text_auto=True, title=f"Number of Product of {geo}",
                       color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_layout(
        hovermode='x',
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors['figure_text'],
        ),
        legend=dict(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color=colors['figure_text']
            ),
            bgcolor=colors['background'],
            borderwidth=5
        ),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        margin=dict(l=0, r=0, t=65, b=0),
        height=350,
        bargap=0.1,
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8010)
