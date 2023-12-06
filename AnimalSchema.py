def animal_update_schema (animal_id=None, species_id=None, new_status=None, new_birth_year=None, enclosure_id=None):

    # sql update animal
    animal_sql = "UPDATE Animal SET"

    # animal data saved for sql
    animal_data = []

    # if staments are used to put in data the user has inputed empty fields will be ignored
    if species_id is not "":
        animal_sql += " SpeciesID = %s,"
        animal_data.append(species_id)

    if new_status is not "":
        animal_sql += " Status = %s,"
        animal_data.append(new_status)

    if new_birth_year is not "":
        animal_sql += " BirthYear = %s,"
        animal_data.append(new_birth_year)

    if enclosure_id is not "":
        animal_sql += " EnclosureID = %s,"
        animal_data.append(enclosure_id)

    # Remove the trailing comma for sql
    animal_sql = animal_sql.rstrip(',')

    # if the set is empty than return
    if animal_data == []:

        return animal_data
        
    # where to say data according to ID
    animal_sql += " WHERE ID = %s"

    # append data to saved data set
    animal_data.append(animal_id)

    return animal_sql, animal_data


def animal_insert_schema(species_id, status, birth_year,enclosure_id):

    # Insert data into the Animal table
    animal_data = [status, birth_year, species_id, enclosure_id]

    # SQL for inserting animal
    animal_sql = "INSERT INTO Animal (Status, BirthYear, SpeciesID, EnclosureID) VALUES (%s, %s, %s, %s)"

    return animal_sql, animal_data


def animal_info(animal_id):

    animal_data = [animal_id,]

    animal_sql = "SELECT * FROM Animal WHERE ID = %s;"\
    
    return animal_sql, animal_data