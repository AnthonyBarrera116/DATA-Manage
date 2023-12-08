# revenue Insert
def revunetype_insert_schema (revenue, number_sold, datetime_sold,reveune_id):

    revunetype_data = [revenue, number_sold, datetime_sold,reveune_id,]

    revunetype_sql = "INSERT INTO RevenueEvents (Revenue, NumberSold, DateTime, RevenueTypeID) VALUES (%s, %s, %s, %s)"

    return revunetype_sql, revunetype_data