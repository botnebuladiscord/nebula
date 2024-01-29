def nebulaisdigit(query):
    query = str(query)
    if query.startswith('-'):
        query = query[1:]
    if '.' in query:
        for i in query:
            if i == '.':
                decimalpoint = query.index(i)
                query = query[:decimalpoint] + query[decimalpoint+1:]
                break
    if query.isdigit():
        return True
    else:
        return False