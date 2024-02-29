def create_polling_id(data, columns=[]):
    output = data[columns[0]].fillna("###").copy()

    for column in columns[1:]:
        output += "-" + data[column].fillna("###").astype(str)
    return output
