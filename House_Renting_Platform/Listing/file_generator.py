import sqlite3
import os

path = "./db.sqlite3"
table_name= "Listing_listingmodel"
filepath=os.path.join(os.getcwd(), "available_properties.txt")
filepath1="Listing/available_properties.txt"
columns_to_fetch = ['id', 'city_address', 'province','location','property_type','title','description','price']

def export_txt():
    try:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        column_str = ", ".join(columns_to_fetch)
        c.execute(f'SELECT {column_str} FROM {table_name}')
        rows = c.fetchall()

        with open(filepath,'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(map(str, rows)) + "\n")

            print("succesfully written the file")


        with open(filepath1,'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(map(str, rows)) + "\n")

            print("succesfully written the file")

        print("your file is written")    


    except sqlite3.Error as e:
        print( "Sorry there was a problem..." )      

    finally:
        if conn:
         conn.close()     