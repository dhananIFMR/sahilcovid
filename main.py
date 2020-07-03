import pandas as pd
from utils.questions import (
    overview_questions,
    business_recovery_questions,
    credit_questions,
    household_challenges_questions,
    employment_questions,
)

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import flask

import base64

from dash.dependencies import Input, Output

from utils.data import read_data
from utils.summary_table import summary_table
from utils.views import index, business, credit, household, employment, playground
from utils.playground import make_charts_for_questions


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)


responses, question_labels = read_data()
label_questions = {v: k for k, v in question_labels.items()}
raw_data = pd.read_csv("./static/data/raw.csv")

unique_type_of_industry = raw_data["TypeofIndustry"].unique()
unique_genders = raw_data[label_questions["Gender"]].unique()
unique_states = raw_data["State"].unique()


app.layout = html.Div(
    className="container-fluid",
    style={"padding-right": "0px", "padding-left": "0px"},
    children=[dcc.Location(id="url", refresh=False), html.Div(id="body")],
)


@app.callback(
    dash.dependencies.Output("body", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return index(responses, summary_table)
    elif pathname == "/business":
        return business(responses)
    elif pathname == "/employment":
        return employment(responses)
    elif pathname == "/credit":
        return credit(responses)
    elif pathname == "/household":
        return household(responses)
    elif pathname == "/playground":
        return playground(unique_states, unique_type_of_industry, unique_genders)


@app.callback(
    Output("playground-data", "children"),
    [
        Input("tabs-example", "value"),
        Input("state-filter", "value"),
        Input("gender-filter", "value"),
        Input("industry-filter", "value"),
        Input("break-down", "value"),
    ],
)
def render_content(tab, state_filter, gender_filter, industry_filter, breakdown):
    if tab == "overview":
        questions = overview_questions
    elif tab == "business_recovery":
        questions = business_recovery_questions
    elif tab == "household":
        questions = household_challenges_questions
    elif tab == "credit":
        questions = credit_questions
    elif tab == "employment":
        questions = employment_questions
    return make_charts_for_questions(
        raw_data,
        questions,
        state_filter,
        gender_filter,
        industry_filter,
        breakdown,
        label_questions,
    )

static_image_route = '/assets/'
image_directory = './assets'

@app.server.route('{}<image_path>'.format(static_image_route))
def serve_image(image_path):
    return flask.send_from_directory(image_directory, image_path)


if __name__ == "__main__":
    app.run_server(port=8080, host="0.0.0.0", debug=True)
