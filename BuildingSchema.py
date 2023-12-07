# reurn building insert sql and data
def building_insert_schema(building_name, building_type):

    building_data = [building_name, building_type]

    building_sql = """INSERT IGNORE INTO Building (Name, Type)VALUES (%s, %s);"""

    return building_sql, building_data


# reurn enclousure insert sql and data
def enclosure_insert_schema(enclosure_id, sq_ft):

    enclosure_data = [sq_ft,enclosure_id]

    enclosure_sql = """INSERT IGNORE INTO Enclosure (SquareFoot, BuildingID)VALUES (%s, %s);"""

    return enclosure_sql, enclosure_data

# retrurns sql and data for updating building
def building_update_schema(building_id, building_name, building_type):

    building_sql = "UPDATE Building SET"

    building_data = []

    if building_name is not "":
        building_sql += " name = %s,"
        building_data.append(building_name)

    if building_type is not "":
        building_sql += " type = %s,"
        building_data.append(building_type)

    building_sql = building_sql.rstrip(',')

    if building_data == []:

        return building_data
        
    building_sql += " WHERE ID = %s"

    building_data.append(building_id)

    return building_sql, building_data

def building_info_by_name(building_name):

    building_data = [building_name,]

    building_sql = "SELECT * FROM Building WHERE Name = %s;"
    
    return building_sql, building_data

def building_info_by_ID(building_id):

    building_data = [building_id,]

    building_sql = "SELECT * FROM Building WHERE ID = %s;"
    
    return building_sql, building_data
