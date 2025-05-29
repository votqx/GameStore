import mysql.connector

def Execute(sqlStatement=""):
    connect = mysql.connector.connect(host="localhost",user="root",password="root",database="gamestore")
    myCursor = connect.cursor()
    myCursor.execute(sqlStatement)
    connect.commit()

def Select(sqlStatement=""):
    connect = mysql.connector.connect(host="localhost",user="root",password="root",database="gamestore",port="3306")
    myCursor = connect.cursor()
    myCursor.execute(sqlStatement)
    result = myCursor.fetchall()
    connect.commit()

    return result

def AutoID(field="", table="", prefix=""):
    sql = f"SELECT {field} FROM {table}"
    ids = []

    # Fetch data from the table
    records = Select(sql)

    if records:
        # Extract numeric parts of the IDs
        ids = [int(record[0][len(prefix):]) for record in records]  # Remove the prefix and convert to int
        next_id = max(ids) + 1  # Find the maximum numeric ID and increment
    else:
        next_id = 1  # Start at 1 if no records exist

    # Format the new ID without digit limitations
    strID = f"{prefix}{next_id:06}"  # Adjust this format if you want more/less leading zeros

    return strID

def display(dataList=[]):
    for i in dataList:
        print(i)
    
    #print(int('000010'))
    #AutoID("gameID","game","G")