# revune insert
def revunetype_insert_schema (name_attraction):

    revunetype_data = [name_attraction,'Entertainment',]

    revunetype_sql = "INSERT INTO RevenueType (Name, Type) VALUES (%s, %s)"

    return revunetype_sql, revunetype_data

# Attraction Insert
def attraction_insert_schema (s_price, a_price,c_price,num_show,num_req,species_id):

    revunetype_data = [s_price, a_price,c_price,num_show,num_req,species_id,]

    revunetype_sql = "INSERT INTO animalshow (SeniorPrice, AdultPrice,ChildPrice, NumberPerDay, NumberRequested, SpeciesID,RevenueTypeID) VALUES (%s, %s,%s, %s,%s, %s,%s)"

    return revunetype_sql, revunetype_data

# Attractuion update
def attraction_update_schema (attraction_id, s_price,a_price,c_price,num_show):

    attraction_sql = "UPDATE AnimalShow SET"

    attraction_data = []
        
    if s_price is not "":
        attraction_sql += " SeniorPrice = %s,"
        attraction_data.append(s_price)

    if a_price is not "":
        attraction_sql += " AdultPrice = %s,"
        attraction_data.append(a_price)
        
    if c_price is not "":
        attraction_sql += " ChildPrice = %s,"
        attraction_data.append(c_price)

    if num_show is not "":
        attraction_sql += " NumberPerDay = %s,"
        attraction_data.append(num_show)

    attraction_sql = attraction_sql.rstrip(',')

    if attraction_data == []:

        return attraction_data
        
    attraction_sql += " WHERE ID = %s"

    attraction_data.append(attraction_id)

    return attraction_sql, attraction_data
