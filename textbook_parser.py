import fitz

doc = fitz.open(r"C:\Users\kyl3g\Downloads\Biochemistry and Molecular Biology 6th edition (Snape, Alison, Papachristodoulou, Despo etc.) (Z-Library).pdf")
start_page = 36

text = ""
for page_num in range(start_page, len(doc)):
    page = doc[page_num]
    text += page.get_text()

with open("biochem_textbook_output.txt", "w", encoding="utf-8") as f:
    f.write(text)