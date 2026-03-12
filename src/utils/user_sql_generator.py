def build_table_insert_sql(table: str, data: dict, start_index: int):
    """
    table: имя таблицы
    data: поля таблицы
    start_index: с какого номера начинаются $1, $2, ...
    """
    fields = list(data.keys())
    placeholders = [f"${i}" for i in range(start_index, start_index + len(fields))]

    sql = f"""
    INSERT INTO {table} ({", ".join(fields)})
    VALUES ({", ".join(placeholders)})
    """.strip()

    return sql, list(data.values()), start_index + len(fields)


def build_tables_insert_sql(tables: dict) -> (dict, list):
    sql_parts = []
    params_to_query = []
    queries = []
    index = 1

    # порядок: от родителя к наследнику
    for table in reversed(list(tables.keys())):
        data = tables[table]
        sql, part_params, _ = build_table_insert_sql(table, data, index)
        sql_parts.append(sql)
        queries.append((sql, part_params))
        params_to_query.append(part_params)

    final_sql = ";\n".join(sql_parts) + ";"
    return queries

