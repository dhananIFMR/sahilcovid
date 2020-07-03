import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from utils.charts import make_question_pie, make_household_multi
from utils.summary_table import make_summary_table
from utils.playground import make_playground_header


def make_jumbotron(link_text, link_href):
    jumbotron = dbc.Jumbotron(
        [
            html.Div(
                children=[
                    html.Img(src="/assets/ifmr-logo.png", className="ifmrlogo"),
                    html.Img(src="/assets/game-logo.png", className="gamelogo"),
                ],
                className="head-box container",
            ),
            html.H2("COVID-19 Dashboard", className="app-header"),
            html.P(
                """
                    COVID-19 and the preventive measures for it such as the lockdown in
                    multiple countries has affected the economy worldwide.
                    In India, in particular, where microbusinesses form the foundation
                    of a significant amount of livelihoods and source of employment
                    the effects of the lockdown are significant.""",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(dcc.Link(link_text, href=link_href), className="lead"),
            html.P(html.A("Download the Dataset", href="/download-data"), className="lead"),
        ]
    )
    return jumbotron


def index(responses, summary_table):
    business_recovery_data_plot = make_question_pie(
        responses, "Confidence in business recovery"
    )
    cash_recovery_plot = make_question_pie(
        responses, "How much cash reserves do you currently have?"
    )
    employment_plot = make_question_pie(responses, "Were employees laid off?")
    household_plot = make_household_multi(
        responses, "Challenges in the household during lockdown (multiple choice)"
    )
    row_style = {}
    return [
        dbc.Row(make_jumbotron("View the Playground", "/playground")),
        dbc.Row(html.H3("Overview"), className="overview"),
        dbc.Row(
            className="overviewtbl",
            children=[dbc.Col(make_summary_table(responses, summary_table))],
        ),
        dbc.Row(
            style=row_style,
            children=[
                dbc.Col(
                    children=[
                        html.H3(dcc.Link("Business Recovery", href="business")),
                        business_recovery_data_plot,
                    ]
                )
            ],
            className="businview",
        ),
        # html.Hr(className="my-2"),
        dbc.Row(
            style=row_style,
            children=[
                dbc.Col(
                    children=[
                        html.H3(
                            dcc.Link("Credit/Loans/Financial Status", href="credit")
                        ),
                        cash_recovery_plot,
                    ]
                )
            ],
            className="finview",
        ),
        # html.Hr(className="my-2"),
        dbc.Row(
            style=row_style,
            children=[
                dbc.Col(
                    children=[
                        html.H3(dcc.Link("Employment", href="employment")),
                        employment_plot,
                    ]
                )
            ],
            className="empview",
        ),
        # html.Hr(className="my-2"),
        dbc.Row(
            style=row_style,
            children=[
                dbc.Col(
                    children=[
                        html.H3(dcc.Link("Houeshold Challenges", href="household")),
                        household_plot,
                    ]
                )
            ],
            className="houseview",
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
    plot_types = ["pie", "bar", "bar", "bar", "bar", "bar", "bar", "bar", "bar", "bar"]
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
                dbc.Row(dbc.Col(make_household_multi(responses, question, barmode="stack", orientation="h")))
            )
    return [make_jumbotron("Back to Overview", "/")] + plot_list


def credit(responses):
    questions = [
        "How much cash reserves do you currently have?",
        "Did you dip into your savings",
        "Did you postpone any loan repayment due to cash crunch?",
        "Did you try borrowing to cover expenses?",
        "Were you able to secure a loan?",
        "Where did you get the loan from? (multiple choice)",
        "Payment to suppliers this month",
        "Payment to suppliers next month",
        "Are you getting paid by your customers",
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
        "bar",
        "bar",
        "bar",
        "bar",
        "bar",
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
