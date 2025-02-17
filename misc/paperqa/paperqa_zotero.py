from collections import defaultdict
import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
from paperqa.litqa import read_litqa_v2_from_hub
from pydantic import BaseModel
from paperqa import Docs
from paperqa.contrib import ZoteroDB
from llmclient import (
    LiteLLMModel,
    LiteLLMEmbeddingModel
)
import litellm


is_env_loaded = load_dotenv(".env")
print(f"Is .env loaded: {is_env_loaded}")


# from litellm import completion
# import os

# ## set ENV variables
# response = completion(
#   model="openai/openai_o1",
#   api_key=os.getenv("OPENAI_API_KEY"),
#   api_base=os.getenv("OPENAI_BASE_URL"),
#   messages=[{ "content": "Hello, how are you?","role": "user"}]
# )

# breakpoint()

model_list_llm = [{ # list of model deployments 
    "model_name": "openai/openai_gpt4o_mini", # model alias -> loadbalance between models with same `model_name`
    "litellm_params": { # params for litellm completion/embedding call 
        "model": "openai/openai_gpt4o_mini", # actual model name
        "api_key": os.getenv("OPENAI_API_KEY"),
        "api_base": os.getenv("OPENAI_BASE_URL"),
    }
}]

model_list_embed = [
    {
        "model_name": "openai/openai_text_embedding_ada", # model alias -> loadbalance between models with same `model_name`
        "litellm_params": { # params for litellm completion/embedding call 
            "model": "openai/openai_text_embedding_ada", # actual model name
            "api_key": os.getenv("OPENAI_API_KEY"),
            "api_base": os.getenv("OPENAI_BASE_URL"),
    }
    }
]


def create_docs(start: int = 0, limit: int=200, collection_name: str="paperqa") -> Docs:
    docs = Docs()
    zotero = ZoteroDB(library_type="user")  # "group" if group library
    litellm.api_base = os.getenv("OPENAI_BASE_URL")
    llm_model = LiteLLMModel(name="openai/openai_gpt4o_mini", config={"model_list": model_list_llm})
    embedding_model = LiteLLMEmbeddingModel(
        name="openai/openai_text_embedding_ada", config={"model_list": model_list_embed}
    )
    # llm_model = LiteLLMModel(config={"model_list": model_list})

    for item in zotero.iterate(start=start, limit=limit, collection_name=collection_name):
        if item.num_pages > 30:
            continue  # skip long papers
        docs.add(
            item.pdf, 
            docname=item.key, 
            llm_model=llm_model,
            embedding_model=embedding_model,
        )
    return docs


class Page(BaseModel):
    paper_title: str = None
    page_name: str = None # title+page eg. "desautels2024computationallyrestoringthe pages 2-2"
    text: str = None
    doi: str = None
    doi_url: str = None
    doc_url: str = None


class ParsedDoc(BaseModel):
    paper_title: str = None
    full_text: str = None
    doi: str = None
    doi_url: str = None
    doc_url: str = None
    page_numbers: List[str] =[]  # List to store page numbers


def save_pages_to_parquet(pages: List[Page], filename: str):
    # Convert list of Page instances to a list of dictionaries
    pages_data = [page.dict() for page in pages]
    
    # Create a pandas DataFrame
    df_pages = pd.DataFrame(pages_data)
    
    # Write the DataFrame to a Parquet file
    df_pages.to_parquet(filename, index=False)


def load_pages_from_parquet(filename: str) -> List[Page]:
    # Read the Parquet file into a pandas DataFrame
    df_pages = pd.read_parquet(filename)
    
    # Convert the DataFrame to a list of Page instances
    pages = [Page(**row) for index, row in df_pages.iterrows()]
    
    return pages


def concat_pages_to_docs(pages: List[Page]) -> List[ParsedDoc]:
    """Concatenate pages with the same DOI into a single document.

    Args:
        pages (List[Page]): _description_

    Returns:
        List[ParsedDoc]: _description_
    """
    # Group pages by DOI
    grouped_docs = defaultdict(list)
    for page in pages:
        grouped_docs[page.doi].append(page)

    # Create a Docs instance for each group
    doc_list = []
    for doi, pages_group in grouped_docs.items():
        # Sort pages based on page_name (assuming page_name can be used for sorting)
        # sorted_pages = sorted(pages_group, key=lambda p: p.page_name)
        full_text = " ".join(page.text for page in pages_group)
        
        # Collect page numbers from page_name or extract them accordingly
        page_numbers = [page.page_name for page in pages_group]  # or any logic to extract page numbers
       
        # Assuming paper_title and URLs are the same for all pages in the group
        paper_title = pages_group[0].paper_title
        doi_url = pages_group[0].doi_url
        doc_url = pages_group[0].doc_url
        
        doc_list.append(ParsedDoc(
            paper_title=paper_title,
            doi=doi,
            full_text=full_text,
            doi_url=doi_url,
            doc_url=doc_url,
            page_numbers=page_numbers
        ))

    return doc_list


def append_full_text(row, parsed_docs):
    for doc in parsed_docs:
        if doc.doi_url in row.sources:
            row["full_text"].append({doc.doi_url: doc.full_text})
    return row


def add_full_text_to_train_dataset(parsed_docs):
    # parsed_docs = concat_pages_to_docs(pages)

    train, eval, test = read_litqa_v2_from_hub()
    

    train["full_text"] = [[] for _ in range(len(train))]
    train.apply(append_full_text, axis=1, args=(parsed_docs,))

    # train[train.full_text.str.len() > 0]
    return train


def main():
    docs = create_docs(start=10, limit=100, collection_name="paperqa")
    pages = []
    for idx, text in enumerate(docs.texts):
        try:
            page = Page(
                paper_title=text.doc.title,
                page_name=text.name,
                text=text.text,
                doi=text.doc.doi,
                doi_url=text.doc.doi_url,
                doc_url=text.doc.url,
            )
            pages.append(page)
            print(f"{idx} done: {page.page_name}")
        except Exception as e:
            print(f"Error: {e}")
    
    save_pages_to_parquet(pages, "pages_p2.parquet")


if __name__ == "__main__":
    main()


# (Pdb) docs.docs["7b40aa8e5568238b"].doi
# '10.1038/s41467-023-41318-2'
# (Pdb) docs.docs["7b40aa8e5568238b"].doi_url
# 'https://doi.org/10.1038/s41467-023-41318-2'

#text, name, doi_url
# # name: 'desautels2024computationallyrestoringthe pages 2-2'
# docs.texts[idx].name

# docs.texts[0].doc.docname
# # 'desautels2024computationallyrestoringthe'

# # raw text: page content. terrible... 1 row is not a sentence.. it is a concat of 1 row from 2 columns...
# docs.texts[0].text

# # doi_url/ doi:
# docs.texts[idx].doc.doi_url

# docs.texts[1].doc.pages
# '878-885'

# docs.texts[1].doc.url
# 'https://www.nature.com/articles/s41586-024-07385-1.pdf'

# docs.texts[1].doc.title
# 'Computationally restoring the potency of a clinical antibody against Omicron'
# docs.texts[1].doc.citation_count
6

#     # Write to parquet
#     df_docs.to_parquet(filename, index=False)

# def load_docs_from_parquet(filename: str) -> Docs:
#     # Read the Parquet file
#     df_docs = pd.read_parquet(filename)

#     # Reconstruct the docs dictionary
#     docs = {row['key']: row['value'] for _, row in df_docs.iterrows()}

#     # Prepare to create the Docs instance
#     # You may need custom logic to handle texts_index and other complex types
#     return Docs(
#         id=UUID(df_docs['id'][0]),
#         docs=docs,
#         name=df_docs['name'][0],
#         deleted_dockeys=set(df_docs['deleted_dockeys'][0]),
#         docnames=set(df_docs['docnames'][0]),
#         texts=df_docs['texts'][0],
#         texts_index=df_docs['texts_index'][0]  # You may need to deserialize further
#     )
