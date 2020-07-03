import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from utils.charts import make_question_pie, make_household_multi
from utils.summary_table import make_summary_table
from utils.playground import make_playground_header


def make_jumbotron(link_text, link_href):
    jumbotron = dbc.Jumbotron(
        [   html.Div( children=[
                        html.Img(src="/assets/lead-logo-new.png" , className="ifmrlogo"),
                        html.Img(src="/assets/game-logo.png" , className="gamelogo"),
                    ],
                    className="head-box container", ),
                        html.Div( children=[
                           html.H2("Impact of COVID-19 on Microenterprises in India", className="app-header"),
                            html.Div( children=[
                           html.H3("Introduction", className ="sub-head"),
                           html.P("""
                    The LEAD/GAME COVID-19 survey is being conducted with an aim to capture the status of micro-enterprises in India during COVID-19, through dynamic multidimensional survey of various microbusiness over a period of 6 months. This will allow us to get insights at a granular level and to take a quick pulse overtime (short-term/long-term perception).""",
                className="lead"),
                
                html.P("""
               A new collaborative study by GAME and LEAD at Krea University seeks to capture the status of micro-enterprises in India during the COVID-19 crisis. Through a multidimensional survey of microbusinesses being conducted over six months (time period?), the study will capture key trends on the impact of the COVID crisis and government-mandated lockdowns on business livelihoods, employment, and the income of nano and microbusinesses.  Additionally, the survey will also provide reliable estimates on business and employment outcomes and gauge confidence levels of small businesses in the economy periodically.
.""",
                className="lead"),
 html.Br(className=""),
                html.P(""" This dashboard presents results from the ongoing survey and allows visitors to explore and visualise the data.""",
                className="lead"),
               
                  
                       ],
                        className="desbox"
                        ),
                           
                            html.Div( children=[
 html.H3("Survey Methodology", className ="sub-headrgt"),
                  html.P("""
                    Our stratified, convenience sample was drawn from various sub-industries in manufacturing, services and trade to provide a sectoral representation of microbusinesses. The sample was selected from lists provided by partner organizations. The following regions and states will be covered in the survey: North India (Delhi, Haryana, Punjab, Uttar Pradesh), South India (Tamil Nadu), West India (Gujarat, Maharashtra, Rajasthan). The surveys were conducted telephonically in the area’s local language, and each survey took 18-25 minutes to administer .""",
                className="leadrgt"),

                        ],
                        className="desbox"
                        ),

                        ],
                        className="head-text"
                        ),
            html.Hr(className="my-2"),
            html.P(dcc.Link(link_text, href=link_href), className="lead"),
        ]
    )
    return jumbotron


def index(responses, summary_table):
    business_recovery_data_plot = make_question_pie(
        responses, "Confidence in business recovery"
    )
    cash_recovery_plot = make_question_pie(
        responses, "How much cash reserves do you have?"
    )
    employment_plot = make_question_pie(responses, "Were employees laid off?")
    household_plot = make_household_multi(
        responses, "Challenges in the household during lockdown (multiple choice)"
    )
    row_style = {
              
    }
    return [
        dbc.Row(make_jumbotron("Explore", "/playground")),
        dbc.Row(
            html.H3("Overview"), className ="overview"
        ),
        dbc.Row(
            className ="overviewtbl",
            children=[dbc.Col(make_summary_table(responses, summary_table))],
        ),
        dbc.Row(
            style=row_style,
            children=[
                dbc.Col(
                    children=[
                        html.H3(dcc.Link("Business Recovery", href="business")),
                        business_recovery_data_plot,
                    ],
                   
                )
            ],
            className ="businview",
        ),
        #html.Hr(className="my-2"),
        dbc.Row(
            style=row_style,
            children=[
                dbc.Col(
                    children=[
                        html.H3(
                            dcc.Link("Credit/Loans/Financial Status", href="credit")
                        ),
                        cash_recovery_plot,
                    ],
                   
                )
            ],
             className ="finview",
        ),
        #html.Hr(className="my-2"),
        dbc.Row(
            style=row_style,
            children=[
                dbc.Col(
                    children=[
                        html.H3(dcc.Link("Employment", href="employment")),
                        employment_plot,
                    ],
                     
                )
            ],
             className ="empview",
        ),
        #html.Hr(className="my-2"),
        dbc.Row(
            style=row_style,
            children=[
                dbc.Col(
                    children=[
                        html.H3(dcc.Link("Houeshold Challenges", href="household")),
                        household_plot,
                    ],
                    
                )
            ],
              className ="houseview",
        ),
    ]


def business(responses):
    questions = [
        "Business Type",
        "Confidence in business recovery",
        "Business Status During Lockdown",
        "Category of Business",
        "Business Registration",
        "Business performance compared expectation in a no-lockdown scenario",
        "Challenges in operation",
        "Coping strategies adopted (multiple choice)",
        "Expected time of business recovery",
        "Intention to apply for relief",
    ]
    plot_types = ["pie", "bar", "bar", "bar", "bar", "bar", "pie", "pie", "bar", "bar"]
    plot_list = []
    for question, plot_type in zip(questions, plot_types):
        if plot_type == "pie":
            plot_list.append(dbc.Row(dbc.Col(make_question_pie(responses, question))))
        if plot_type == "bar":
            plot_list.append(
                dbc.Row(dbc.Col(make_household_multi(responses, question)))
            )
    return [make_jumbotron("Back to Overview", "/")] + plot_list


def employment(responses):
    questions = ["Were employees laid off?"]
    plot_types = ["bar"]
    plot_list = []
    for question, plot_type in zip(questions, plot_types):
        if plot_type == "pie":
            plot_list.append(dbc.Row(dbc.Col(make_question_pie(responses, question))))
        if plot_type == "bar":
            plot_list.append(
                dbc.Row(dbc.Col(make_household_multi(responses, question)))
            )
    return [make_jumbotron("Back to Overview", "/")] + plot_list


def credit(responses):
    questions = [
        "How much cash reserves do you have?",
        "Did you dip into your savings",
        "Did you postpone any loan repayment due to cash crunch?",
        "Did you try borrowing to cover expenses?",
        "Were you able to secure a loan?",
        "Where did you get the loan from? (multiple choice)",
        "Payment to suppliers this month",
        "Payment to suppliers next month",
        "Are you getting paid by your customers?",
        "Use of digital payments",
        "How long have you been using these digital payments for your business?",
        "Overall, how do you think your usage of digital payments has changed during the lockdown?",
        "For what purposes has your usage of digital payments changed during the lockdown?",
        "Why do you think there has been a change in the use of digital payments?",
    ]
    plot_types = [
        "bar",
        "bar",
        "pie",
        "bar",
        "bar",
        "bar",
        "bar",
        "bar",
        "bar",
        "pie",
        "pie",
        "pie",
        "pie",
        "pie",
    ]
    plot_list = []
    for question, plot_type in zip(questions, plot_types):
        if plot_type == "pie":
            plot_list.append(dbc.Row(dbc.Col(make_question_pie(responses, question))))
        if plot_type == "bar":
            plot_list.append(
                dbc.Row(dbc.Col(make_household_multi(responses, question)))
            )
    return [make_jumbotron("Back to Overview", "/")] + plot_list


def household(responses):
    questions = [
        "Are you the sole earner for the household?",
        "Challenges in the household during lockdown (multiple choice)",
    ]
    plot_types = ["bar", "bar"]
    plot_list = []
    for question, plot_type in zip(questions, plot_types):
        if plot_type == "pie":
            plot_list.append(dbc.Row(dbc.Col(make_question_pie(responses, question))))
        if plot_type == "bar":
            plot_list.append(
                dbc.Row(dbc.Col(make_household_multi(responses, question)))
            )
    return [make_jumbotron("Back to Overview", "/")] + plot_list


def playground(unique_states, unique_type_of_industry, unique_genders):
    playground = [
        dbc.Row(
            children=dbc.Col(
                make_playground_header(
                    unique_states, unique_type_of_industry, unique_genders
                )
            ),
            style={"padding-left": "50px", "padding-right": "50px"},
        )
    ]
    return [make_jumbotron("Back to Overview", "/")] + playground
