from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.cache import cache




def home(request):
    update_spreadsheets()
    cache.clear()
    return render(request,'index.html')

def upload(request):
    if request.method == 'POST':
        filepath = request.FILES.get('document', False)
        print(filepath)
        if filepath != False:

            #uploaded_file = request.FILES['document']
            uploaded_file = request.FILES['document']
            #print(uploaded_file)
            #print(uploaded_file.name)


            print(request.POST)
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            print("files uploaded")



            process_spreadsheets()
            print("files proccesed")


            clear_downloads()
            print("files cleared")
            return HttpResponseRedirect('/')


    return HttpResponseRedirect('/')

def remove_colums(request):
    if request.method == 'POST':
        colum = request.POST['lname']
        spreadsheet_parse(colum)
        pass


    return HttpResponseRedirect('/')

def clear(request):
    clear_database()

    #return render(request,'index.html')
    return HttpResponseRedirect('/')







#the following code has to be here because django cant import it
#just pretend its in a diffrent file
# !!!!!! the / might need to be changed to // to function in linux
import os
import sqlite3
import pandas as pd
from pathlib import Path




#### update spreadsheets function attached to home url
def update_spreadsheets():
    conn = sqlite3.connect((os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "db.sqlite3"))
    #load csv filepath
    csv_path = (os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "static") + "/" + "spreadsheets.csv"

    xl_path = (os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "static") + "/" + "spreadsheets.xlsx"

    json_path = (os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "static") + "/" + "data.json"

    txt_path = (os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "static") + "/" + "data.txt"

    sql_conn = sqlite3.connect((os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "static") + "/" + "spreadsheet.sqlite3")


    sql_path = (os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "static") + "/" + "spreadsheet.sqlite3"

    sql_data = pd.read_sql_query("SELECT * from spreadsheets", conn)
    render_data = sql_data.drop(columns=['blank'])
    #wipe csv file
    csv_file = open(csv_path, 'r+')
    csv_file.truncate(0)
    csv_file.close()

    xl_file = open(xl_path, 'r+')
    xl_file.truncate(0)
    xl_file.close()

    #load sql_data into csv file
    render_data.to_csv (csv_path, index = False, header=True)

    render_data.to_excel(xl_path, index = False)

    with open(json_path, 'r+') as json_file:
        json_file.truncate(0)
        json_file.write(render_data.to_json(orient="columns"))

    with open(txt_path, 'r+') as txt_file:
        txt_file.truncate(0)
        render_data.to_string(txt_file)

    #load sql data
    sql_file = open(sql_path, 'r+')
    sql_file.truncate(0)
    sql_file.close()
    sql_data.to_sql(name="spreadsheets",con=sql_conn,index=False)

    print("this is the sql data")
    print(sql_data)


    conn.close()
    sql_conn.close()





####### upload URL function
def process_spreadsheets():
    media_path = (os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "media")
    for root, dirs, files in os.walk(media_path):
        for f in files:
            file_path = os.path.join(root, f)
            name, extension = os.path.splitext(file_path)
            if extension == '.xlsx':
                print(file_path)
                proccess_xls(file_path)

            if extension == '.csv':
                #pass
                proccess_csv(file_path)
def proccess_xls(xl_path):
    import openpyxl
    excelframe = pd.read_excel(xl_path, engine='openpyxl')
    dataframes = [excelframe]
    compactframes = pd.concat(dataframes)
    #print(compactframes)

    add_to_sql(compactframes)

def proccess_csv(csv_path):
    csvframe = pd.read_csv (csv_path)
    dataframes = [csvframe]
    compactframes = pd.concat(dataframes)
    #print(compactframes)

    add_to_sql(compactframes)





def add_to_sql(unparsed_dataframe):
    dataframe = remove_spaces(unparsed_dataframe)
    conn = sqlite3.connect((os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "db.sqlite3"))
    tablenames = []
    tablenames_path = (os.path.dirname(os.path.abspath(__file__))) + "/" + "tablenames.txt"
    #unwanted_columns = []
    with open(tablenames_path, 'r+') as file:
        for line in file:
            data = line.replace("\n", "")
            tablenames.append(data)
        for column in dataframe.columns:
            if containsNumber(column) == True or column == "Unnamed: 0":
                dataframe.drop(columns=[column])
                pass
            #if containsNumber(column) == True:
                #print(column)
                #print("\n")
                #unwanted_columns.append(column)
                #pass
            else:
                if column not in tablenames:
                    print(column)
                    conn.execute("""ALTER TABLE spreadsheets
                    ADD """ + column + " VARCHAR(100)")
                    file.write(column)
                    file.write("\n")

    file.close()

    #print(pd.read_sql("SELECT * FROM *", conn))
    #for unwanted_column in unwanted_columns:
        #dataframe.drop(columns=[unwanted_column])dataframe.drop(columns=[colum])
    #sql_dataframe = dataframe.drop(columns=[""])
    dataframe.to_sql(name="spreadsheets", if_exists='append', con=conn,index=False)
    conn.commit()
    conn.close()

def remove_spaces(dataframe):
    for colum in dataframe.columns:
        if containsNumber(colum) == True:
            print("/n")
            print(colum)
            pass
            #dataframe.drop(columns=[colum])
            #pass
            #print(colum + "data is int")
            #dataframe.drop(columns=[colum])
            #print(coulum + "data is string")
        #i think the str is causing a near zer0 syntax error
        else:
            dataframe.rename(columns={ colum: colum.replace(" ","_")},
                      inplace=True)
    print(dataframe)
    return dataframe
def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False





def clear_downloads():
    media_path = (os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "media")
    for root, dirs, files in os.walk(media_path):
        for f in files:
            filepath = os.path.join(root, f)
            os.remove(filepath)





####### remove URL function
def spreadsheet_parse(unwanted_data):
    tablenames = []
    tablenames_path = (os.path.dirname(os.path.abspath(__file__))) + "/" + "tablenames.txt"
    #unwanted_columns = []
    with open(tablenames_path, 'r+') as file:
        for line in file:
            data = line.replace("\n", "")
            tablenames.append(data)
    file.close()

    conn = sqlite3.connect((os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "db.sqlite3"))

    #load sql data into data dataframe
    sql_data = pd.read_sql_query("SELECT * from spreadsheets", conn)

    if unwanted_data in tablenames:

        new_data = sql_data.drop(columns=[unwanted_data,'blank'])

        clear_database()

        add_to_sql(new_data)

        conn.commit()
    else:
        pass

    conn.close()






####### clear URL function
def clear_database():
    tablenames_path = (os.path.dirname(os.path.abspath(__file__))) + "/" + "tablenames.txt"
    file = open(tablenames_path, 'r+')
    file.truncate(0)
    file.close()

    database = open((os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "db.sqlite3"), 'r+')
    database.truncate(0)
    database.close()

    json_path = open((os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "static") + "/" + "data.json", 'r+')
    json_path.truncate(0)
    json_path.close()

    conn = sqlite3.connect((os.path.dirname(os.path.abspath(__file__))).replace("app_engine", "db.sqlite3"))
    conn.execute("""CREATE TABLE spreadsheets(blank)""")
    conn.commit()
    conn.close()
