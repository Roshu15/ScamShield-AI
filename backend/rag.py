from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/phishing.pdf")

documents = loader.load()

print(f"Loaded {len(documents)} pages")

print("\nFirst 500 characters:\n")

print(documents[0].page_content[:500])