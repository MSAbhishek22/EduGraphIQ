import os
import time
import networkx as nx
import matplotlib.pyplot as plt
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pyvis.network import Network
import webbrowser

# Load environment variables (if needed)
load_dotenv()

# Set Groq API key directly
os.environ["GROQ_API_KEY"] = "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"

# Load and read the PDF
pdf_path = "C:/Users/hp/Desktop/EduGraphIQ/pdfs/sample.pdf"
if not os.path.exists(pdf_path):
    print(f"File not found: {pdf_path}")
    exit()

print("Loading PDF...")
loader = PyPDFLoader(pdf_path)
pages = loader.load()[:10]  # ✅ Limit to first 10 pages
print("Extracting concepts and building knowledge graph...")

# Split text into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,  # ✅ Reduced chunk size
    chunk_overlap=100
)
chunks = text_splitter.split_documents(pages)

# Initialize Groq LLM
llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="llama3-8b-8192"
)

# Create prompt template
prompt = PromptTemplate.from_template(""" 
You are an expert AI tutor. Analyze the academic content below and extract key concepts and how they relate to each other. 
Format output as a list of concept pairs like: Concept A -> Concept B.

Content:
{input}
""")

chain = prompt | llm | StrOutputParser()

# Build knowledge graph
G = nx.DiGraph()

for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i+1}/{len(chunks)}...")
    success = False
    retries = 3

    while not success and retries > 0:
        try:
            output = chain.invoke({"input": chunk.page_content})
            pairs = [line.split("->") for line in output.split("\n") if "->" in line]
            for pair in pairs:
                if len(pair) == 2:
                    src, dst = pair[0].strip(), pair[1].strip()
                    G.add_edge(src, dst)
            success = True
        except Exception as e:
            if "rate_limit_exceeded" in str(e).lower():
                print("Rate limit hit. Waiting 2 minutes before retrying...")
                time.sleep(120)
                retries -= 1
            else:
                print(f"Error extracting from chunk: {e}")
                break

# Draw knowledge graph using matplotlib (static version)
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=2000, font_size=10)

# Remove emoji and keep the title simple
plt.title("Concept Graph from PDF")
try:
    plt.tight_layout()
except:
    pass  # Handles potential warning
plt.show()

# Interactive graph with pyvis
net = Network(notebook=False)
for node in G.nodes:
    net.add_node(node)
for src, dst in G.edges:
    net.add_edge(src, dst)

# Save the interactive graph as an HTML file
net.show("graph_interactive.html")

# Automatically open the HTML file in the browser
webbrowser.open("graph_interactive.html")
