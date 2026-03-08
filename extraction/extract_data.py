import os
import json
import pandas as pd
import mysql.connector

# -----------------------------
# MySQL Connection
# -----------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="phonepe_db"
)

cursor = conn.cursor()

base_path = "../dataset"

# -----------------------------
# 1. AGGREGATED TRANSACTION
# -----------------------------

data = []

path = base_path + "/aggregated/transaction/country/india/state"

for state in os.listdir(path):

    state_path = os.path.join(path, state)

    for year in os.listdir(state_path):

        year_path = os.path.join(state_path, year)

        for file in os.listdir(year_path):

            quarter = file.replace(".json","")

            with open(os.path.join(year_path,file)) as f:

                content = json.load(f)

                for i in content['data']['transactionData']:

                    name = i['name']
                    count = i['paymentInstruments'][0]['count']
                    amount = i['paymentInstruments'][0]['amount']

                    data.append([state,year,quarter,name,count,amount])


df = pd.DataFrame(data)

for row in df.itertuples(index=False):

    cursor.execute("""
    INSERT INTO aggregated_transaction
    VALUES (%s,%s,%s,%s,%s,%s)
    """,tuple(row))

conn.commit()

print("Aggregated Transaction Done")


# -----------------------------
# 2. AGGREGATED USER
# -----------------------------

data = []

path = base_path + "/aggregated/user/country/india/state"

for state in os.listdir(path):

    state_path = os.path.join(path,state)

    for year in os.listdir(state_path):

        year_path = os.path.join(state_path,year)

        for file in os.listdir(year_path):

            quarter = file.replace(".json","")

            with open(os.path.join(year_path,file)) as f:

                content = json.load(f)

                try:
                    for i in content["data"]["usersByDevice"]:

                        data.append([
                            state,
                            year,
                            quarter,
                            i["brand"],
                            i["count"],
                            i["percentage"]
                        ])
                except:
                    pass


df = pd.DataFrame(data)

for row in df.itertuples(index=False):

    cursor.execute("""
    INSERT INTO aggregated_user
    VALUES (%s,%s,%s,%s,%s,%s)
    """,tuple(row))

conn.commit()

print("Aggregated User Done")


# -----------------------------
# 3. MAP TRANSACTION
# -----------------------------

data = []

path = base_path + "/map/transaction/hover/country/india/state"
print(os.listdir(base_path + "/map"))
for state in os.listdir(path):

    state_path = os.path.join(path,state)

    for year in os.listdir(state_path):

        year_path = os.path.join(state_path,year)

        for file in os.listdir(year_path):

            quarter = file.replace(".json","")

            with open(os.path.join(year_path,file)) as f:

                content = json.load(f)

                for i in content["data"]["hoverDataList"]:

                    data.append([
                        state,
                        year,
                        quarter,
                        i["name"],
                        i["metric"][0]["count"],
                        i["metric"][0]["amount"]
                    ])


df = pd.DataFrame(data)

for row in df.itertuples(index=False):

    cursor.execute("""
    INSERT INTO map_transaction
    VALUES (%s,%s,%s,%s,%s,%s)
    """,tuple(row))

conn.commit()

print("Map Transaction Done")


# -----------------------------
# 4. MAP USER
# -----------------------------

data = []

path = base_path + "/map/user/hover/country/india/state"

for state in os.listdir(path):

    state_path = os.path.join(path,state)

    for year in os.listdir(state_path):

        year_path = os.path.join(state_path,year)

        for file in os.listdir(year_path):

            quarter = file.replace(".json","")

            with open(os.path.join(year_path,file)) as f:

                content = json.load(f)

                for district,data1 in content["data"]["hoverData"].items():

                    data.append([
                        state,
                        year,
                        quarter,
                        district,
                        data1["registeredUsers"],
                        data1["appOpens"]
                    ])


df = pd.DataFrame(data)

for row in df.itertuples(index=False):

    cursor.execute("""
    INSERT INTO map_user
    VALUES (%s,%s,%s,%s,%s,%s)
    """,tuple(row))

conn.commit()

print("Map User Done")


# -----------------------------
# 5. TOP TRANSACTION
# -----------------------------

data = []

path = base_path + "/top/transaction/country/india/state"

for state in os.listdir(path):

    state_path = os.path.join(path,state)

    for year in os.listdir(state_path):

        year_path = os.path.join(state_path,year)

        for file in os.listdir(year_path):

            quarter = file.replace(".json","")

            with open(os.path.join(year_path,file)) as f:

                content = json.load(f)

                for i in content["data"]["districts"]:

                    data.append([
                        state,
                        year,
                        quarter,
                        i["entityName"],
                        i["metric"]["count"],
                        i["metric"]["amount"]
                    ])


df = pd.DataFrame(data)

for row in df.itertuples(index=False):

    cursor.execute("""
    INSERT INTO top_transaction
    VALUES (%s,%s,%s,%s,%s,%s)
    """,tuple(row))

conn.commit()

print("Top Transaction Done")


# -----------------------------
# CLOSE CONNECTION
# -----------------------------

conn.close()

print("All Data Inserted Successfully")