#import psycopg2
import mysql.connector
import json
import base64

# POSTGRESQL CONNECTION
# DB_NAME = 'degilib'
# DB_PASSWORD = '140053'
# DB_HOST = '10.2.42.53'

# conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
# cur = conn.cursor()

conn = mysql.connector.connect(
    host="10.2.42.50",
    user="root",
    password="140053",
    database="degilib"
)
cur = conn.cursor()


# MYSQL CONNECTION
mydb = mysql.connector.connect(
    host="10.2.42.48",
    user="root",
    password="DEVINE"
    # database="db_a274eb_cbsua"
)
mycursor = mydb.cursor()


# ------- mydb0 FUNCTIONS

def checkduplicate(barcode):
    sql = 'SELECT * FROM `degilib`.`fileStorage` WHERE filename = %s;'
    data = (barcode,)
    cur.execute(sql, data)
    res = cur.fetchall()
    # conn.close()
    print(str(len(res)) + " entry already in system")
    return len(res)


def in_to_tb(metadata, val, campus, fname, taon):
    rawd = json.dumps(metadata)
    sql1 = "INSERT INTO `degilib`.`metadata`  (title,author,taon,call_number,barcode,abstract,kurso,filename,subjek,raw_data, col,campus)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (metadata["Title"], metadata["Author"], taon, metadata["Info"], metadata["Barcode"], metadata["Abstract"], metadata["Course"], fname, metadata["Subject"], rawd, val, campus)
    cur.execute(sql1, val)
    print(cur.rowcount, "record inserted.")
    conn.commit()
    # conn.close()



def intoFileStorage(data):
    # rawd = json.dumps(data)
    val = (data["filename"], data["datab64"])
    sql = 'INSERT INTO `degilib`.`fileStorage`  (filename, data) VALUES (%s, %s);'
    cur.execute(sql, val)
    print(cur.rowcount, "base64 copy of the file uploaded successfully.")
    conn.commit()
    # conn.close()



# ------- MYSQL FUNCTIONS

def myFunction(bcodes):  # select data from db
    sql = "SELECT * FROM `db_a274eb_cbsua`.`books` WHERE Maintext like %s limit 2"
    if bcodes != "":
        aa = bcodes.split(".")
        bcode = aa[0];
        fll = ("%" + bcode + "%",)
    mycursor.execute(sql, fll)
    myresult = mycursor.fetchall()
    for x in myresult:
        return x


# print(myFunction('T0006249.pdf'))


# --- Utilities


def makeDic(res):
    title = decon(res, "<001>", "<002>")
    author = decon(res, "<002>", "<003>")
    institution = decon(res, "<003>", "<004>")
    kuros = decon(res, "<004>", "<005>")
    taon = decon(res, "<005>", "<006>")
    info = decon(res, "<007>", "<008>")
    barcode = decon(res, "<008>", "<009>")
    subject = decon(res, "<0012>", "<0013>")
    abstract = decon(res, "<0013>", "<0014>")
    metadata = {
        "Title": title,
        "Author": author,
        "Institution": institution,
        "Course": kuros,
        "Year": taon,
        "Info": info,
        "Barcode": barcode,
        "Subject": subject,
        "Abstract": abstract
    }
    return metadata


def decon(result, bago, huri):
    var1 = result[1].split(bago)
    var2 = var1[1].split(huri)
    var3 = var2[0].replace("\x1e", "")
    return var3


def conVB64(filename):
    data = open(filename, "rb").read()
    encoded = base64.b64encode(data)
    return {'filename': filename, 'datab64': encoded}

# raw bytes
def conBuffer(filename):
    data = open(filename, "rb").read()
    return {'filename': filename, 'datab64': data}
