def create_polling_id(data, columns=[]):
    output = data[columns[0]].copy()

    for column in columns[1:]:
        output += "-" + data[column].astype(str)
    return output
