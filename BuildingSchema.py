def building_insert_schema(building_name, building_type):

    # Insert data into the Building table
    building_data = [building_name, building_type]

    # SQL for inserting Building
    building_sql = """INSERT IGNORE INTO Building (Name, Type)VALUES (%s, %s);"""

    return building_sql, building_data


def enclosure_insert_schema(enclosure_id, sq_ft):

    # Insert data into the Building table
    enclosure_data = [sq_ft,enclosure_id]

    # SQL for inserting Building
    enclosure_sql = """INSERT IGNORE INTO Enclosure (SquareFoot, BuildingID)VALUES (%s, %s);"""

    return enclosure_sql, enclosure_data

def building_update_schema(building_id, building_name, building_type):

    # sql update Building
    building_sql = "UPDATE Building SET"

    # Building data saved for sql
    building_data = []

    # if staments are used to put in data the user has inputed empty fields will be ignored
    if building_name is not "":
        building_sql += " name = %s,"
        building_data.append(building_name)

    if building_type is not "":
        building_sql += " type = %s,"
        building_data.append(building_type)

    # Remove the trailing comma for sql
    building_sql = building_sql.rstrip(',')

    # if the set is empty than return 2 and error nothing updated empty fields
    if building_data == []:

        # empty fields
        return building_data
        
    # where to say data according to ID
    building_sql += " WHERE ID = %s"

    # append data to saved data set
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
