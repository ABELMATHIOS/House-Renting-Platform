from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os

load_dotenv()


file_path = os.path.join(os.getcwd(), "available_properties.txt")

raw_documents = TextLoader(file_path,encoding="utf-8").load()

text_splitter = CharacterTextSplitter(chunk_size=0,chunk_overlap=0,separator="\n")

documents = text_splitter.split_documents(raw_documents)

db_properties = Chroma.from_documents(documents,embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))


def Recommendatons(query, k):
    recommendations = db_properties.similarity_search(query, k)
    similar_properties = []

    for i in range(6):
        property_id = recommendations[i].page_content.split()[0].strip('(').strip(',')

        similar_properties.append(int(property_id))




    return similar_properties
