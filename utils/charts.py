import copy

import dash_core_components as dcc

colors = ['#005DA6', '#FFC52F', '#BAE1FF', '#75C2FF', '#31A4FF', '#00467D', '#CBC53E'] * 5

def make_question_pie(responses, question):
    business_recovery_data = responses[question]
    first_key = list(responses[question].keys())[0]
    p_key = None
    for k in responses[question][first_key].keys():
        if k.startswith("Percentage"):
            p_key = k
            break
    business_recovery_data = {
        k: float(v[p_key].replace("%", "")) for k, v in business_recovery_data.items()
    }
    business_recovery_data_keys, business_recovery_data_values = zip(
        *business_recovery_data.items()
    )
    data = [
        {
            "values": business_recovery_data_values,
            "labels": business_recovery_data_keys,
            "type": "pie",
             'marker': {
              'colors': [
                '#005DA6',
'#FFC52F',
'#BAE1FF',
'#75C2FF',
'#31A4FF',
'#00467D',
'#CBC53E',
'#0199D6',
'#6D6E71',

              ]
            },
        }
    ]
    business_recovery_data_plot = dcc.Graph(
        id=question,
        className="graphbox",
        figure={"data": data, "layout": {"height": "200px", "title": question}},
    )
    return business_recovery_data_plot


def make_household_multi(responses, question):
    household_data = copy.deepcopy(responses[question])
    for key in household_data.keys():
        if household_data[key].get("Freq"):
            household_data[key].pop("Freq")
        if household_data[key].get("Percentage"):
            household_data[key].pop("Percentage")
        if household_data[key].get("Percentage of case"):
            household_data[key].pop("Percentage of case")
        household_data[key] = {k: v / responses["Total Sample"].get(k, 1) * 100 for k, v in household_data[key].items()}
    data_list = []
     #colors = ['lightslategray',] * 5
    for key in household_data.keys():
        columns, values = zip(*household_data[key].items())
        data_list.append(
            {
                "x": columns,
                "y": values,
                "type": "bar",
                "name": key,
                #'marker': {"color": colors}
            }
        )
    fig = dcc.Graph(
        id="household",
        className="graphbox",
        figure={
            "data": data_list,
            "layout": {
                "title": {"text": question},
                "barmode": "group",
                "yaxis": {"title": "% of Responses"},
            },
        },
    )
    return fig
