import mysql.connector
from re import search
import json
import base64
import psycopg2

mydb = mysql.connector.connect(
    host="10.2.42.48",
    user="root",
    password="DEVINE"
    # database="db_a274eb_cbsua"
)

mycursor = mydb.cursor()

mydb1 = mysql.connector.connect(
    host="10.2.42.50",
    user="root",
    password="140053"
    # database="db_a274eb_cbsua"
)
mycursor1 = mydb1.cursor()

DB_NAME = 'degilib'
DB_USER = 'postgres'
DB_PASSWORD = '140053'
DB_HOST = '10.2.42.53'

mydb2 = psycopg2.connect(dbname=DB_NAME, user= DB_USER, password= DB_PASSWORD, host= DB_HOST)
mycursor2 = mydb2.cursor()


def myFunction(bcodes):  # select data from db
    # print("function 1")
    sql = "SELECT * FROM `db_a274eb_cbsua`.`books` WHERE Maintext like %s limit 2"
    if bcodes != "":
        aa = bcodes.split(".")
        bcode = aa[0];
        fll = ("%" + bcode + "%",)
    mycursor.execute(sql, fll)
    myresult = mycursor.fetchall()
    for x in myresult:
        return x


def checkduplicate(barcode):
    sql = "SELECT * FROM `digilib-demo`.`fileStorage` WHERE filename like '" + barcode + "';"
    mycursor1.execute(sql)
    myresult = mycursor1.fetchall()
    print(str(len(myresult)) + " entry already in system")
    return len(myresult)


def in_to_tb(metadata, val, campus, fname):
    # mycursor = mydb.cursor()
    rawd = json.dumps(metadata)
    sql1 = "INSERT INTO `digilib-demo`.`metadata` (`title`,`author`,`taon`,`call_number`,`barcode`,`abstract`,`kurso`,`filename`,`subjek`,`raw_data`, `col`,`campus`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (metadata["Title"], metadata["Author"], metadata["Year"], metadata["Info"], metadata["Barcode"],
           metadata["Abstract"], metadata["Course"], fname, metadata["Subject"], rawd, val, campus)
    sql = "INSERT INTO `digilib-demo`.`metadata` (`title`,`author`,`call_number`,`barcode`,`abstract`,`kurso`,`institution`,`subjek` ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    mycursor1.execute(sql1, val)
    mydb1.commit()
    print(mycursor1.rowcount, "record inserted.")


def intoFileStorage(data):
    # rawd = json.dumps(data)
    val = (data["filename"], data["datab64"])
    sql = "INSERT INTO `digilib-demo`.`fileStorage` (`filename`,`data`) VALUES (%s, %s);"
    mycursor1.execute(sql, val)
    mydb1.commit()
    print(mycursor1.rowcount, "base64 copy of the file uploaded successfully.")


def decon(result, bago, huri):
    var1 = result[1].split(bago)
    var2 = var1[1].split(huri)
    var3 = var2[0].replace("\x1e", "")
    return var3


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


def conVB64(filename):
    data = open(filename, "rb").read()
    encoded = base64.b64encode(data)
    return {'filename': filename, 'datab64': encoded}
