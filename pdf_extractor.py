import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_from_pdf(pdf_path):
    pdf = fitz.open(pdf_path)
    slides_data = []

    for page_num, page in enumerate(pdf, start=1):
        # Get text
        text = page.get_text().strip()

        # Get images
        images_data = []
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]  # image reference
            base_image = pdf.extract_image(xref)
            img_bytes = base_image["image"]
            images_data.append(img_bytes)

        slides_data.append({
            "page": page_num,
            "text": text,
            "images": images_data
        })

    return slides_data

def ocr_image(img_bytes):
    image = Image.open(io.BytesIO(img_bytes))
    return pytesseract.image_to_string(image).strip()

def process_pdf(pdf_path):
    slides_data = extract_from_pdf(pdf_path)
    processed_slides = []

    for slide in slides_data:
        combined_text = slide["text"]

        for img_bytes in slide["images"]:
            # OCR
            ocr_text = ocr_image(img_bytes)
            if ocr_text:
                combined_text += "\n[Diagram Text]: " + ocr_text

            # Caption (optional, if you have a caption_image function)
            # caption = caption_image(img_bytes)
            # combined_text += "\n[Diagram Caption]: " + caption

        processed_slides.append({
            "page": slide["page"],
            "content": combined_text
        })

    return processed_slides

slides_data = process_pdf(r"C:\Users\kyl3g\Downloads\4 Fertilization to Gastrulation FA25.pdf")
print(slides_data)