def fetchData(connection, columns, table, **kwargs):

    # Function to fetch data from postgres DB
    # kwargs:
    # rowsToFetch: int number of rows to fetch
    # conditions: list of conditions to search for

    query = f'select {columns} from {table}'

    if 'conditions' in kwargs:
        conditions = kwargs['conditions']
        conditionsList = []

        for key in conditions.keys():
            conditionsList.append(key + ' = ' + "'{}'" .format(conditions[key]))
            
        conditionsList = ' and '.join(conditionsList)

        query = query + ' where ' + conditionsList


    if 'conditionsOr' in kwargs:
        conditions = kwargs['conditionsOr']
        conditionsList = []

        for key in conditions.keys():
            conditionsList.append(key + ' = ' + "'{}'" .format(conditions[key]))
            
        conditionsList = ' or '.join(conditionsList)

        query = query + ' where ' + conditionsList


    if 'rowsToFetch' in kwargs:
        rowsToFetch = kwargs['rowsToFetch']
        
        query = query + f' fetch first {rowsToFetch} rows only'

    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results