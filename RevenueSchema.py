# revenue Insert
def revunetype_insert_schema (name,revenue, number_sold, datetime_sold,reveune_id):

    revunetype_data = [name,revenue, number_sold, datetime_sold,reveune_id,]

    revunetype_sql = "INSERT INTO RevenueEvents (name,Revenue, NumberSold, StartDate, RevenueTypeID) VALUES (%s,%s, %s, %s, %s)"

    return revunetype_sql, revunetype_data

def revenue_report(date):
    revenue_sql = """SELECT EventID, Name, Revenue, NumberSold, StartDate, RevenueType.Type AS RevenueSource
            FROM RevenueEvents
            JOIN RevenueType ON RevenueEvents.RevenueTypeID = RevenueType.ID
            WHERE StartDate = %s;
            """
    revenue_data = [date]
    return revenue_sql, revenue_data


def produce_rep():
    revenue_sql = []

    revenue_sql.append("""SELECT S.Name AS Species, A.Status, COUNT(A.ID) AS Population
                    FROM Animal A
                    JOIN Species S ON A.SpeciesID = S.ID
                    GROUP BY S.Name, A.Status
                    ORDER BY S.Name, A.Status;
                    """)
            
    revenue_sql.append("""SELECT S.Name AS Species, SUM(S.FoodCost) AS MonthlyFoodCost
                    FROM Species S
                    GROUP BY S.Name
                    ORDER BY S.Name;
                    """)

    revenue_sql.append("""SELECT E.FirstName, E.LastName, E.JobType, SUM(HR.RateEarned * 40 * 4) AS MonthlyCost
                    FROM Employee E
                    LEFT JOIN HourlyRate HR ON E.ID = HR.ID
                    WHERE E.JobType IN ('Veterinarian', 'Animal Care')
                    GROUP BY E.FirstName, E.LastName, E.JobType
                    ORDER BY E.JobType, E.FirstName, E.LastName;
                    """)

    revenue_data = []
    return revenue_sql, revenue_data


def top_rep(start_date,end_date):
    revenue_sql = """SELECT EventID, Name AS AttractionName, SUM(Revenue) AS TotalRevenue
            FROM RevenueEvents
            WHERE StartDate BETWEEN %s AND %s
            GROUP BY EventID, Name
            ORDER BY TotalRevenue DESC
            LIMIT 3;

            """
    revenue_data = [start_date,end_date]
    return revenue_sql, revenue_data

def best_rep(month,year):
    revenue_sql = """SELECT StartDate AS RevenueDate, SUM(Revenue) AS TotalRevenue
            FROM RevenueEvents
            WHERE MONTH(StartDate) = %s AND YEAR(StartDate) = %s 
            GROUP BY StartDate
            ORDER BY TotalRevenue DESC
            LIMIT 5;

            """
    revenue_data = [month,year]
    return revenue_sql, revenue_data

def avg_rep(start_date,end_date):

    revenue_sql = []

    revenue_sql.append("""SELECT EventID, Name AS EventName, AVG(Revenue) AS AverageRevenue
            FROM RevenueEvents
            WHERE StartDate BETWEEN %s AND %s 
            GROUP BY EventID, Name;

                    """)

    revenue_sql.append("""SELECT NULL AS EventID, 'Total Attendance' AS EventName, AVG(NumberSold) AS AverageAttendance
            FROM RevenueEvents
            WHERE StartDate BETWEEN %s AND %s;

                    """)
    revenue_data = [start_date,end_date]
    return revenue_sql, revenue_data

