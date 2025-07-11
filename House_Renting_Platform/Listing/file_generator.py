import sqlite3
import os

path = "./db.sqlite3"
table_name= "Listing_listingmodel"
filepath=os.path.join(os.getcwd(), "available_properties.txt")
filepath1="Listing/available_properties.txt"
columns_to_fetch = ['id', 'city_address', 'province','location','property_type','title','description','price']
operation_status_success=False
is_available_properties_empty = True

def export_txt():
    global operation_status_success
    global is_available_properties_empty
    try:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        column_str = ", ".join(columns_to_fetch)
        c.execute(f'SELECT {column_str} FROM {table_name}')
        rows = c.fetchall()

        with open(filepath,'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(map(str, rows)) + "\n")

        with open(filepath1,'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(map(str, rows)) + "\n")

            print("SUCCESS: succesfully written the text file!!!")

        print("SUCCESS: 'available_properties.txt' is updated successfully!!!") 
        operation_status_success = True  

        with open(filepath1, 'r') as f:
            content = f.read().strip()
            
            if bool(content):
                is_available_properties_empty = False
            else:
                is_available_properties_empty = True

    except sqlite3.Error as e:
        print( "PROBLEM: Sorry there was a problem...I couldn't write 'available_properties.txt' file!!!" )  
        operation_status_success = False    

    finally:
        if conn:
         conn.close()
        print(f"Operation is Successfull: {operation_status_success}")   



export_txt()      