# from langchain_ollama import OllamaEmbeddings
# from langchain_chroma import Chroma
# from langchain_core.documents import Document
# import os
# import pandas as pd


# # df = pd.read_csv("handbook.csv")
# df = pd.read_csv("handbook.csv", on_bad_lines='skip')                   
# embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# db_location = "./chroma_db"
# add_documents = os.path.exists(db_location)

# if add_documents:
#     documents =[]
#     vector_store = Chroma(
#     # ... other parameters (keep everything else)
# )
#     # ids = []

#     for i, row in df.iterrows():
#         document = Document(
#             page_content=row["Title"] + " " + row["Content"],
#             metadata={"rating": row["Rating"], "date": row["Date"]},
#             id=str(i)
#         )

#         ids.append(str(i))
#         documents.append(document)

# vector_store = Chroma(
#     collection_name="handbook",
#     embedding_function=embeddings,
#     persist_directory=db_location,
#     ids=ids if add_documents else None
# )

# if add_documents:
#     vector_store.add_documents(documents=documents, ids=ids)

# retriever = vector_store.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 5}
# )









from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_db"
# Check if database doesn't exist (meaning we need to add documents)
should_add_documents = not os.path.exists(db_location)

# Initialize the vector store
vector_store = Chroma(
    collection_name="bible_data_set",
    embedding_function=embeddings,
    persist_directory=db_location
)

# Add documents if database doesn't exist
if should_add_documents:
    documents = []
    ids = []
    
    # Read the text file and parse it
    with open("bible_data_set.csv", "r", encoding="utf-8") as file:
        content = file.read()
    
    # Split by triple semicolons to get sections
    sections = content.split(";;;")
    
    # Remove empty sections and process each one
    sections = [section.strip() for section in sections if section.strip()]
    
    for i, section in enumerate(sections):
        if section:  # Only process non-empty sections
            # Use the first line as title if it exists, otherwise use section number
            lines = section.split('\n')
            title = lines[0].strip() if lines else f"Section {i+1}"
            content_text = section.strip()
            
            document = Document(
                page_content=f"{title}\n\n{content_text}",
                metadata={
                    "section_number": i+1,
                    "title": title,
                    "source": "bible_data_set"
                }
            )
            
            ids.append(f"section_{i+1}")
            documents.append(document)
    
    print(f"Created {len(documents)} documents from the bible_data_set")
    
    # Add documents to the vector store
    if documents:
        vector_store.add_documents(documents=documents, ids=ids)
        print("Documents added to vector store")
    else:
        print("No documents found to add")

# Create retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Adjust k as needed
)