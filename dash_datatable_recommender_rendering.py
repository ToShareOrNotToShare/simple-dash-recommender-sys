from dash import Dash
from dash import dash_table as dt
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

from recommender_sys_calculations import *

# suppressing chained calculation warnings, comment if you want them to reappear for checks
pd.set_option('mode.chained_assignment',None)


def create_dash_data_table_with_recommendations(df, column ,top_n):

    """Prints customized welcome string based on time

    Args: 
        df              (object):   DataFrame
        column          (string):   Name of the column
        top_n           (integer):  Amount of top recommendations to show in data table

    Returns:
        app             (object):   The Dash application consisting of a datatable

    """



    ########## future: could also take comments and first step into account? ###########

    static_view_title = df[column].iloc[0]

    static_recommendation = initialize_frame_for_recommender(df,
                                                static_view_title,column,top_n)

    """    # prototype which is always displayed
    static_view_open_tasks = df.head(top_n)"""


    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout =    dbc.Container([
                        dbc.Row([
                            html.Div([
                            
                            html.Div([
                                dcc.Input(id='input-1-submit', type='text', placeholder='What do you feel like doing?', 
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
                                                children=f'Top {top_n} Recommendations for "{static_view_title}"',
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

            new_recommendations = initialize_frame_for_recommender(df,
                                                    value ,'texts',top_n, True)

            new_recommendations.reset_index(drop = True, inplace=True)

            recommendations_title = f'Top {top_n} Recommendations for "{value}"'

            # setting values for integrating the data from dataframe into the datatable
            return new_recommendations.to_dict('records'), recommendations_title

    return app

                        



if __name__ == '__main__':

    # example data input
    data = [
            ['About the job Job name: Machine Learning and Data Engineer'],
            ['Job type: Full time (100%)'],
            ['Location: Zürich, Switzerland (possibility to work remotely, depending on experience)'],
            ['Description Are you attracted by the opportunity to work at an exciting European travel tech startup, contributing to developing the technological backbone?'],
            ['If so, we can’t wait to hear from you!'],
            ['About Us The Trip Boutique is an award-winning AI-powered personal travel advisory platform that instantly designs bespoke and bookable travel itineraries.'],
            ['We are looking for a hands-on Machine Learning and Data Engineer'],
            ['With experience in Natural Language Processing in Zürich (Switzerland) to complete our highly talented tech team.'],
            ['You will work directly with our CEO, CTO, Operations Lead and Tech Lead.'],
            ['After raising a seed funding round from high proﬁle investors from the industry'],
            ['We have a fully-fledged product built on state-of-the-art technologies serving thousands of B2C clients as well as B2B partners.'],
            ['What we offer: An exceptional opportunity to help shape and create technology; '],
            ['Take responsibility for an essential part of our product and software development;'],
            ['A chance for you to combine a variety of your tech skills and learn every day;'],
            ['Be part of an innovative, award-winning travel tech start-up;'],
            ['Be involved in different stages of a start-up and be part of scaling up and growing a business;'],
            ['Work on an exciting product;'],
            ['A creative and supportive environment where every team member is encouraged to voice their ideas, thoughts, and visions;'],
            ['Be actively part of a smart, fun-loving and international team with very ambitious goals.'],
            ['Your job includes: Working closely with the CEO, CTO, Operations Lead and the software engineering team to create and improve ML/AI enabled software and products;'],
            ['Helping identify, create and implement data-based, machine-learning and/or AI-based product improvements to meet customer and business demands;'],
            ['Implementing algorithms, models and tools aligned with our data science strategies;'],
            ['Searching for and selecting datasets, processing and cleansing data, and performing data analysis (incl. integrity and quality);'],
            ['Writing reusable, tested and efﬁcient code;'],
            ['Improving and maintaining existing products and software like our recommender system and category predictor;'],
            ['Evaluating and implementing new ML solutions to further scale our products; '],
            ['Documenting code independently;'],
            ['Visualizing and analyzing different kinds of business and/or user data;'],
            ['Improving process automation and scalability;'],
            ['What you bring: Degree in Computer Science, Data Science, Machine Learning or related fields;'],
            ['Proven track record of ML related projects; Previous exposure to Natural Language Processing;'],
            ['Good understanding of Python, min. 2 years; Good understanding of SQL;'],
            ['Good understanding of microservice architecture; Good understanding of Git;'],
            ['English Proﬁciency, written and spoken; Capacity to work on your own and independently;'],
            ['Ability to work in a rapidly evolving startup environment; A personal interest in the travel industry;'],
            ['Passion for creating solutions that make people’s lives easier; Dedication, ﬂexibility and a positive “can-do” attitude.'],
            ['Any of these would be a plus: Experience with Docker; Experience with Message Brokers like RabbitMQ Experience with cloud services (preferably GCP);'],
            ['Experience with Data Visualization tools like Grafana, Tableau or Google Data Studio']

    ]

    df = pd.DataFrame(data, columns = ['texts'])

    # define top n tasks
    top_n = 5

    app = create_dash_data_table_with_recommendations(data, 'texts', 5)


    app.run_server(debug=True)