import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

colors = [	
    "#005DA6",	
    "#BAE1FF",	
    "#75C2FF",	
    "#31A4FF",	
    "#00467D",	
    "#002E53",	
    "#0199D6",	
    "#C4EEFF",	
    "#8ADDFE",	
    "#4FCCFE",	
    "#0173A0",	
    "#004D6B",	
    "#48C1E1",	
    "#DAF3F9",	
    "#B6E6F3",	
    "#91DAED",	
    "#1F9EBF",	
    "#156980",	
    "#CBC53E",	
    "#F5F3D8",	
    "#EAE8B2",	
    "#E0DC8B",	
    "#9D982A",	
    "#68651C",	
    "#FFC52F",	
    "#FFF3D5",	
    "#FFE8AC",	
    "#FFDC82",	
    "#E3A300",	
    "#976D00",	
    "#6D6E71",	
    "#E2E2E3",	
    "#C4C5C6",	
    "#A7A8AA",	
    "#525355",	
    "#363739",	
]
def make_playground_header(unique_states, unique_type_of_industry, unique_genders):
    return [
        dcc.Tabs(
            id="tabs-example",
            value="overview",
            children=[
                dcc.Tab(label="Overview", value="overview", disabled=False),
                dcc.Tab(
                    label="Business Recovery post COVID-19", value="business_recovery"
                ),
                dcc.Tab(label="Credit/Loans/Financial Status", value="credit"),
                dcc.Tab(label="Household Challenges", value="household"),
                dcc.Tab(label="Employment", value="employment"),
            ],
        ),
        make_filters(unique_states, unique_type_of_industry, unique_genders),
        html.Div(children=[], id="playground-data", className="graph-box"),
    ]


def make_filters(unique_states, unique_type_of_industry, unique_genders):
    return dbc.Row(
        children=[
            dbc.Col(
                html.Div(
                    children=[
                        html.P("Break-down by: "),
                        dcc.Dropdown(
                            id="break-down",
                            options=[
                                {"label": i, "value": i} for i in ["Industry", "Gender"]
                            ],
                            style={"width": "250px"},
                        ),
                    ],
                    className="row",
                )
            ),
            dbc.Col(
                html.Div(
                    children=[
                        html.P("Filter by State: "),
                        dcc.Dropdown(
                            id="state-filter",
                            options=[{"label": i, "value": i} for i in unique_states],
                            multi=True,
                            style={"width": "250px"},
                        ),
                    ],
                    className="row",
                )
            ),
            dbc.Col(
                html.Div(
                    children=[
                        html.P("Filter by industry: "),
                        dcc.Dropdown(
                            id="industry-filter",
                            options=[
                                {"label": i, "value": i}
                                for i in unique_type_of_industry
                            ],
                            multi=True,
                            style={"width": "250px"},
                        ),
                    ],
                    className="row",
                )
            ),
            dbc.Col(
                html.Div(
                    children=[
                        html.P("Filter by gender: "),
                        dcc.Dropdown(
                            id="gender-filter",
                            options=[{"label": i, "value": i} for i in unique_genders],
                            multi=True,
                            style={"width": "250px"},
                        ),
                    ],
                    className="row",
                )
            ),
        ],
         className="filter-box",
    )


def make_charts_for_questions(
    data,
    questions,
    state_filter,
    gender_filter,
    industry_filter,
    breakdown,
    label_questions,
):
    breakdown_to_name = {
        "Industry": "TypeofIndustry",
        "Gender": label_questions["Gender"],
    }
    children = []
    for question in questions:
        label = label_questions[question]
        if label in data:
            filtered_df = data
            if state_filter:
                filtered_df = filtered_df[filtered_df["State"].isin(state_filter)]
            if gender_filter:
                filtered_df = filtered_df[
                    filtered_df[label_questions["Gender"]].isin(gender_filter)
                ]
            if industry_filter:
                filtered_df = filtered_df[
                    filtered_df["TypeofIndustry"].isin(industry_filter)
                ]
            if breakdown:
                data_list = []
                unique_vals = filtered_df[breakdown_to_name[breakdown]].unique()
                for un in unique_vals:
                    freqs = filtered_df[
                        filtered_df[breakdown_to_name[breakdown]] == un
                    ][data[label].notna()][label].value_counts()
                    columns = list(freqs.index)
                    values = freqs.to_numpy()
                    data_list.append(	
                        {	
                            "x": columns,	
                            "y": values,	
                            "type": "bar",	
                            "name": un,	
                            "marker": {"color": colors},	
                        }	
                    )
                fig = dcc.Graph(
                    id=label,                   
                    figure={
                        "data": data_list,
                        "layout": {
                            "title": {"text": question},
                            "barmode": "group",
                            "yaxis": {"title": "Responses"},
                         
                        },
                        
                    },
                )
                children.append(dbc.Row(dbc.Col(children=[fig])))
            else:
                freqs = filtered_df[data[label].notna()][label].value_counts()
                columns = list(freqs.index)
                values = freqs.to_numpy()
                fig = dcc.Graph(
                    id=label,                     
                    figure={
                        "data": [
                            {
                                "x": columns,
                                "y": values,
                                "type": "bar",
                                "name": "Responses",
                                "marker": {"color": colors},
                            }
                        ],
                        "layout": {"title": question, "yaxis": {"title": "Responses"}},
                    },
                )
                children.append(dbc.Row(dbc.Col(children=[fig])))
    return children
