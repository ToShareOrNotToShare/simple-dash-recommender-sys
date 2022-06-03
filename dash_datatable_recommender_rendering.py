from dash import Dash
from dash import dash_table as dt
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

from recommender_sys_calculations import *

nltk.download('omw-1.4')

# suppressing chained calculation warnings, comment if you want them to reappear for checks
pd.set_option('mode.chained_assignment',None)

def create_dash_data_table_with_recommendations(df, input_column, output_columns, top_n):

    """Prints customized welcome string based on time

    Args: 
        df              (object):   DataFrame
        input_column    (string):   Name of the text input
        output_columns  (list):   wished columns to display
        top_n           (integer):  Amount of top recommendations to show in data table

    Returns:
        app             (object):   The Dash application consisting of a datatable

    """


    static_view_title = df[input_column].iloc[0]

    """    # get index from title, potentially interesting for cleaner interface
    static_view_index = df.index[df[output_columns] == static_view_title][0]"""

    static_recommendation = initialize_frame_for_recommender(   df,
                                                                static_view_title,
                                                                input_column,
                                                                output_columns,
                                                                top_n)


    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout =    dbc.Container([
                        dbc.Row([
                            html.Div([
                            
                            html.Div([
                                dcc.Input(id='input-1-submit', type='text', placeholder='What do you feel to get recommended?', 
                                # using autocomplete here to let the browser make a judgment
                                autoComplete='on', style={'width': '74%','display': 'inline-block'}),
                                # have some vertical distance below button
                                html.Button('Submit', id='btn-submit', style={'width': '26%','display': 'inline-block',"margin-bottom": "50px"}),
                            ]),

                            ### task recommendations ###

                            html.Div(
                            [
                                html.Div(
                                    [  
                                        html.H3(id='task_recommendations_title',
                                                children=f'Top {top_n} Recommendations for: \n\n"{static_view_title}"',
                                                style={'margin-right': '2em'})
                                    ],
                                ),
                                html.Div([
                                            ############################################
                                            ### Dash DataTable for spreadsheet view ####
                                            ############################################
                                dt.DataTable(
                                    id = 'task_recommendations_table',
                                    # start with the static recommendation first
                                    data = static_recommendation.to_dict('records'),
                                    # display task ID and name 
                                    columns=[{'id': c, 'name': c} for c in static_recommendation.columns],
                                    style_as_list_view=True,
                                    style_cell={'padding': '5px'},
                                    style_header={
                                        'backgroundColor': 'white',
                                        'fontWeight': 'bold'
                                    },
                                    # align these cells left
                                    style_cell_conditional=[
                                        {
                                            'if': {'column_id': c},
                                            'textAlign': 'left'
                                        } for c in ['Name', 'Deadline', 'first step filled']
                                    ],
                                ) 
                                ]),

                                ######## ALTERNATIVE WAY OF DISPLAYING RECOMMENDATIONS? E.G. THROUGH SCATTER / BUBBLEPLOT?

                            ]
                            ),
                            ])
                        ], justify="center", align="center", className="h-50"
                        )
                        ],style={"height": "100vh"})

    ### update the DataTable data###
    @app.callback(
        Output('task_recommendations_table', 'data'),
        Output('task_recommendations_title', 'children'),
        [Input('btn-submit', 'n_clicks')],
        [State('input-1-submit', 'value')])
    def update_data_table(clicked, value):

        """
        Creates new recommendations based on the selected value in the dropdown.
        
        Args:
        n_clicks (int): amount of clicks on submit
        value (string): Name of the task

        Returns:
        df (Dict): df of recommendations in format Dictionary for Dash DataTable
        """

        # always check this for no selection
        if not clicked:

            title = f'Top {top_n} Recommendations for "{static_view_title}"'
            table_data = static_recommendation.to_dict('records')

            return table_data, title

        if clicked:

            print(f'\nthis is our current input value: {value}')

            new_recommendations = initialize_frame_for_recommender( df,
                                                                    value,
                                                                    input_column, 
                                                                    output_columns,
                                                                    top_n,
                                                                    True)

            new_recommendations.reset_index(drop = True, inplace=True)

            recommendations_title = f'Top {top_n} truncated recommendations for "{value}"'

            # setting values for integrating the data from dataframe into the datatable
            return new_recommendations.to_dict('records'), recommendations_title

    return app


if __name__ == '__main__':

    # example data input
    with open('input.txt') as f:
        data = f.readlines()

    cleaned_text = [cleaner(elem) for elem in data]

    cleaned_text_longer_than_one = [elem for elem in cleaned_text if len(elem.split())>1]

    df = pd.DataFrame(cleaned_text_longer_than_one, columns = ['texts'])

    # define top n tasks
    top_n = 5

    app = create_dash_data_table_with_recommendations(df, 'texts', ['texts'], 5)


    app.run_server(debug=True)