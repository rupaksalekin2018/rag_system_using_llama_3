# -*- coding: utf-8 -*-
"""agric_dev_llama_3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1orPGiKmmNsSLBiK3M-7icF96OI9gdTXZ
"""

!python --version

from google.colab import drive
drive.mount('/content/drive')

!pip install marker-pdf
!pip install torch
!pip install torchvision
!pip install torchaudio

# pdf_to_be_markdown = '/content/drive/MyDrive/pdf_to_be_markdown/Hand Book of Agricultural Technology.pdf'
# pdf_to_markdown = '/content/drive/MyDrive/pdf_to_mark_down'

!marker_single '/content/drive/MyDrive/Agric PDFS/Hand Book of Agricultural Technology.pdf' '/content/drive/MyDrive/Agric PDFS/mds/'

!pip install langchain
!pip install langchain-core
!pip install langchain-community

!pip install "unstructured[md]"

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document

markdown_path = "/content/drive/MyDrive/pdf_to_mark_down/Hand Book of Agricultural Technology/Hand Book of Agricultural Technology.md"
loader = UnstructuredMarkdownLoader(markdown_path)

docs = loader.load()

print(docs)

docs[0].page_content

!pip install -qU langchain-text-splitters

from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
    ("#####", "Header 5"),
    ("######", "Header 6"),
]

# MD splits
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, strip_headers=False
)
md_header_splits = markdown_splitter.split_text(docs[0].page_content)

md_header_splits

# Char-level splits
from langchain_text_splitters import RecursiveCharacterTextSplitter

chunk_size = 1000
chunk_overlap = 30


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len,
    is_separator_regex=False
)

# Split
splits = text_splitter.split_documents(md_header_splits)
splits

! pip install --upgrade --quiet  redis

import redis

r = redis.Redis(
  host='redis-13747.c266.us-east-1-3.ec2.redns.redis-cloud.com',
  port=13747,
  password='f5uemiR9otkqKZDhRzf1Uyug6K50cstc')

r.ping()

#r.flushdb() #removes all the keys in the db

! pip install --upgrade --quiet sentence-transformers

from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings()

from langchain_community.vectorstores.redis import Redis

rds = Redis.from_documents(
    splits,
    embeddings,
    redis_url='redis://default:f5uemiR9otkqKZDhRzf1Uyug6K50cstc@redis-13747.c266.us-east-1-3.ec2.redns.redis-cloud.com:13747',
    index_name="agric",
)

rds.index_name

retriever = rds.as_retriever(search_type="similarity", search_kwargs={"k": 10})

retriever.invoke("How to grow rice?")

!pip install colab-xterm

# Commented out IPython magic to ensure Python compatibility.
# %load_ext colabxterm

#curl -fsSL https://ollama.com/install.sh | sh
#ollama serve & ollama run llama3
#ollama serve & ollama run mistral

# Commented out IPython magic to ensure Python compatibility.
# %xterm

# # Find the process ID(s) for 'ollama' and kill them
# pids = !pgrep ollama
# for pid in pids:
#     !kill {pid}

from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

llm.invoke("Who is the president of america?")

llm.invoke("How to grow rice in Bangladesh?")

# Define the temperature
temperature = 0.9  # Adjust the value as needed for accuracy
# Generate text with the specified temperature
# Generate text with the specified temperature
prompt = 'How to grow rice in Dhaka'
response = llm.generate(prompts=[prompt], temperature=temperature)

print(response)

response_text = response.generations[0][0].text

# Print the extracted response text
print(response_text)

from langchain.prompts import ChatPromptTemplate

template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

from langchain_core.output_parsers import StrOutputParser

chain = (
    {"context": (lambda x: x["question"]) | retriever,
     "question": (lambda x: x["question"])}
    | prompt
    | llm
    | StrOutputParser()
)

answer=chain.invoke({"question":"How to raise chickens in Bangladesh?"})

answer

answer=chain.invoke({"question":"How to grow rice in laxmipur, Bangladesh?"})
answer

answer=chain.invoke({"question":"what type of rice is usually grow in Bangladesh?"})
answer

answer=chain.invoke({"question":"what types of rice variant is usually grow in Bangladesh?"})
answer

def format_llm_output_proper_structure(response, words_per_line=20):
    # Split the response into paragraphs
    paragraphs = response.strip().split('\n\n')
    formatted_response = []

    for paragraph in paragraphs:
        # Handle list items separately
        if paragraph.strip().startswith("*"):
            lines = paragraph.strip().split('\n')
            for line in lines:
                if line.strip().startswith("*"):
                    formatted_response.append(line.strip())
                else:
                    formatted_response.extend(insert_line_breaks(line, words_per_line))
        else:
            formatted_response.extend(insert_line_breaks(paragraph, words_per_line))
        formatted_response.append("")  # Add an extra newline for paragraph separation

    return "\n".join(formatted_response).strip()

def insert_line_breaks(text, words_per_line):
    words = text.split()
    lines = []

    for i in range(0, len(words), words_per_line):
        line = " ".join(words[i:i + words_per_line])
        lines.append(line)

    return lines

# Get the readable output with proper structure
readable_output = format_llm_output_proper_structure(answer)
print(readable_output)

answer=chain.invoke({"question":"what types of chicken variant is usually farmed in Bangladesh?"})
# Get the readable output with proper structure
readable_output = format_llm_output_proper_structure(answer)
print(readable_output)

answer=chain.invoke({"question":"what is the grain type of BR22?"})
# Get the readable output with proper structure
readable_output = format_llm_output_proper_structure(answer)
print(readable_output)

answer=chain.invoke({"question":"What are the diseases of rice?"})
# Get the readable output with proper structure
readable_output = format_llm_output_proper_structure(answer)
print(readable_output)

answer=chain.invoke({"question":"What are the diseases of rice in Bangladesh?"})
# Get the readable output with proper structure
readable_output = format_llm_output_proper_structure(answer)
print(readable_output)

answer=chain.invoke({"question":"How to grow rice in Bangladesh?"})
# Get the readable output with proper structure
readable_output = format_llm_output_proper_structure(answer)
print(readable_output)

answer=chain.invoke({"question":"How to farm chicken in Bangladesh?"})
# Get the readable output with proper structure
readable_output = format_llm_output_proper_structure(answer)
print(readable_output)