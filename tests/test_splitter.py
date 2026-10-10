from utils.pdf_loader import PDFLoader
from utils.text_splitter import split_resume

text = PDFLoader.extract_text("Sohail_CV.pdf")

chunks = split_resume(text)

print("=" * 60)
print("Total Chunks:", len(chunks))
print("=" * 60)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print("-" * 30)
    print(chunk[:300])