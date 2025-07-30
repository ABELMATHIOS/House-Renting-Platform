from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
from Listing.file_generator import operation_status_success,is_available_properties_empty

load_dotenv()

is_recommended_properties_available = False

file_path = os.path.join(os.getcwd(), "available_properties.txt")

if operation_status_success == True and is_available_properties_empty == False:

    raw_documents = TextLoader(file_path,encoding="utf-8").load()

    text_splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=0,separator="\n")

    documents = text_splitter.split_documents(raw_documents)

    db_properties = Chroma.from_documents(documents,embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
    
    is_vector_db_created = True

    print("SUCCESS: Succesfully created the vector database!!!")

else:
    is_vector_db_created = False
    print("PROBLEM: There was a problem with creating character embeddings and vector database!!!")    


def Recommendatons(query, k):
    global is_recommended_properties_available
    if is_vector_db_created:
        recommendations = db_properties.similarity_search(query, k)
        similar_properties = []
        for i in range(len(recommendations)):
            property_id = recommendations[i].page_content.split()[0].strip('(').strip(',')

            similar_properties.append(int(property_id))
                
            is_recommended_properties_available=True

            print(f"SUCCESS: Appended the property number {i} to the list")
                
        return similar_properties
        
    else:
        print("PROBLEM: I coudn't access the vector database!!!")
        is_recommended_properties_available = False   
        return None