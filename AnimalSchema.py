# sql and data to update animal
def animal_update_schema (animal_id=None, species_id=None, new_status=None, new_birth_year=None, enclosure_id=None):

    animal_sql = "UPDATE Animal SET"

    animal_data = []

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

    animal_sql = animal_sql.rstrip(',')

    if animal_data == []:

        return animal_data
        
    animal_sql += " WHERE ID = %s"

    animal_data.append(animal_id)

    return animal_sql, animal_data


# sql and data for insert animal
def animal_insert_schema(species_id, status, birth_year,enclosure_id):

    animal_data = [status, birth_year, species_id, enclosure_id]

    animal_sql = "INSERT INTO Animal (Status, BirthYear, SpeciesID, EnclosureID) VALUES (%s, %s, %s, %s)"

    return animal_sql, animal_data

# sql and data for info of  animal
def animal_info(animal_id):

    animal_data = [animal_id,]

    animal_sql = "SELECT * FROM Animal WHERE ID = %s;"\
    
    return animal_sql, animal_data