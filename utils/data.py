from collections import defaultdict
import json

import pandas as pd


def get_total_sample_row(data):
    for key in data[2].keys():
        if data[2][key].strip() == "Total Sample":
            return key


def get_row_values(data, row_number, max_col):
    return [
        data[i][row_number]
        for i in range(0, max_col)
        if data.get(i) and data[i].get(row_number)
    ]


def has_numbers(data):
    for x in data:
        try:
            float(x.strip().replace("%", ""))
            return True
        except Exception as e:
            pass
    return False


def read_data():

    with open("./assets/Sector-based Summary.json", "r") as f:
        raw_data = json.load(f)

    sheet_data = defaultdict(dict)
    for x in raw_data:
        row = int(x["row"])
        col = int(x["col"])
        sheet_data[col][row] = x["$t"]

    rows = []
    question_row = {}
    question_label = {}
    for key in sheet_data[1].keys():
        if sheet_data[1][key][0].lower() != sheet_data[1][key][0]:
            if sheet_data[1][key][1].isnumeric():
                question = sheet_data[2][key].strip()
                question_row[question] = key
                question_label[sheet_data[1][key].replace(".", "").lower()] = question
                rows.append(key)

    rows = sorted(rows)
    next_question_row = {}
    for i in range(len(rows) - 1):
        next_question_row[rows[i]] = rows[i + 1]

    responses = {}
    max_col = max(sheet_data.keys())
    total_sample_row = get_total_sample_row(sheet_data)
    responses["Total Sample"] = {}
    for i in range(total_sample_row, max_col):
        if sheet_data[i]:
            if sheet_data[i].get(total_sample_row):
                if sheet_data[i].get(total_sample_row - 1):
                    responses["Total Sample"][
                        sheet_data[i][total_sample_row - 1]
                    ] = int(sheet_data[i][total_sample_row])
                else:
                    responses["Total Sample"]["Freq"] = int(
                        sheet_data[i][total_sample_row]
                    )

    for row in question_row.keys():
        rowNumber = question_row[row]
        rowData = get_row_values(sheet_data, rowNumber, max_col)
        if has_numbers(rowData):
            headers = get_row_values(sheet_data, rowNumber - 1, max_col)
            if len(headers):
                keys = ["Freq"] + headers
                values = rowData[2:]
                responses[row] = dict(zip(keys, values))
        else:
            if "Response-based%" in rowData:
                validCols = []
                for i in range(2, len(rowData)):
                    if rowData[i] != "Segment%":
                        if rowData[i] != "Response-based%":
                            validCols.append(i + 1)
                responses[row] = {}
                nextQuestionRowNumber = next_question_row.get(
                    rowNumber, max([x for x in sheet_data[2].keys() if x])
                )
                for i in range(rowNumber + 1, nextQuestionRowNumber - 1):
                    if sheet_data[2].get(i):
                        responses[row][sheet_data[2][i]] = {}
                        for j in range(len(validCols)):
                            try:
                                responses[row][sheet_data[2][i]][
                                    rowData[validCols[j] - 1]
                                ] = float(sheet_data[validCols[j]][i])
                            except:
                                responses[row][sheet_data[2][i]][
                                    rowData[validCols[j] - 1]
                                ] = sheet_data[validCols[j]][i]
            else:
                validCols = []
                for i in range(3, max_col):
                    if sheet_data[i].get(rowNumber):
                        validCols.append(i)
                responses[row] = {}
                nextQuestionRowNumber = next_question_row.get(
                    rowNumber, max([x for x in sheet_data[2].keys() if x])
                )
                for i in range(rowNumber + 1, nextQuestionRowNumber - 1):
                    if sheet_data[2].get(i):
                        responses[row][sheet_data[2][i]] = {}
                        for j in range(len(validCols)):
                            try:
                                responses[row][sheet_data[2][i]][
                                    sheet_data[validCols[j]][rowNumber]
                                ] = float(sheet_data[validCols[j]][i])
                            except:
                                responses[row][sheet_data[2][i]][
                                    sheet_data[validCols[j]][rowNumber]
                                ] = sheet_data[validCols[j]][i]
    return responses, question_label
