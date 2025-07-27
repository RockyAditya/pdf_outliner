# extract_outline.py
#
# import os
# import json
# from PyPDF2 import PdfReader
#
# def extract_outline_from_pdf(file_path):
#     reader = PdfReader(file_path)
#     title = reader.metadata.title or os.path.basename(file_path)
#
#     outline = []
#
#     for page_number, page in enumerate(reader.pages):
#         text = page.extract_text()
#         if not text:
#             continue
#
#         for line in text.split("\n"):
#             line_clean = line.strip()
#             if not line_clean:
#                 continue
#
#             # Simple logic: All UPPERCASE → H1, Short line (<5 words) → H2
#             if line_clean.isupper():
#                 outline.append({"level": "H1", "text": line_clean, "page": page_number + 1})
#             elif len(line_clean.split()) < 5:
#                 outline.append({"level": "H2", "text": line_clean, "page": page_number + 1})
#             else:
#                 pass  # ignore other lines
#
#     return {
#         "title": title,
#         "outline": outline
#     }
#
# # Directories
# input_dir = "/app/input"
# output_dir = "/app/output"
#
# # Process all PDFs in the input folder
# for filename in os.listdir(input_dir):
#     if filename.lower().endswith(".pdf"):
#         pdf_path = os.path.join(input_dir, filename)
#         json_data = extract_outline_from_pdf(pdf_path)
#
#         output_filename = filename.replace(".pdf", ".json")
#         output_path = os.path.join(output_dir, output_filename)
#
#         with open(output_path, "w") as f:
#             json.dump(json_data, f, indent=2)
#
#         print(f"Processed {filename} → {output_filename}")

#############################################################################################################
#
# import os
# import json
# import pdfplumber
# import re
# from collections import defaultdict
#
# # Heading detection patterns
# VALID_HEADING_REGEX = [
#     r"^[A-Z][A-Za-z\s:/\-()0-9]+$",
#     r"^[A-Z\s]{4,}$",
#     r"^.*(Responsibilities|Skills|Rules|PRIZES|QUALIFICATIONS|GOVERNING LAW|SPONSORS).*$",
#     r"^[A-Z].{3,50}[:]?$"
# ]
#
# def matches_heading_patterns(text):
#     for pattern in VALID_HEADING_REGEX:
#         if re.match(pattern, text.strip(), re.IGNORECASE):
#             return True
#     return False
#
# def extract_outline_from_pdf(file_path):
#     outline = []
#     title = None
#     font_counter = defaultdict(int)
#
#     def is_bold(fontname):
#         return any(x in fontname.lower() for x in ["bold", "bd", "black"])
#
#     all_text_lines = []
#
#     with pdfplumber.open(file_path) as pdf:
#         for page_num, page in enumerate(pdf.pages, 1):
#             chars = page.chars
#             lines_by_y = defaultdict(list)
#
#             for char in chars:
#                 y0 = round(char["top"], 1)
#                 lines_by_y[y0].append(char)
#
#             for y, chars_on_line in lines_by_y.items():
#                 chars_sorted = sorted(chars_on_line, key=lambda c: c["x0"])
#
#                 text = ""
#                 prev_char = None
#                 for c in chars_sorted:
#                     if prev_char:
#                         gap = c["x0"] - prev_char["x1"]
#                         if gap > 1.5:  # Insert space for visual gap
#                             text += " "
#                     text += c["text"]
#                     prev_char = c
#
#                 text = text.strip()
#                 if not text or len(text) < 4:
#                     continue
#
#                 font_sizes = [round(c["size"], 1) for c in chars_sorted]
#                 avg_size = round(sum(font_sizes) / len(font_sizes), 1)
#                 fonts = [c.get("fontname", "").lower() for c in chars_sorted]
#                 bold = any(is_bold(f) for f in fonts)
#
#                 if bold and matches_heading_patterns(text):
#                     all_text_lines.append({
#                         "text": text,
#                         "font_size": avg_size,
#                         "page": page_num
#                     })
#                     font_counter[avg_size] += 1
#
#         # Determine H1 and H2 font sizes
#         sorted_fonts = sorted(font_counter.items(), key=lambda x: (-x[1], -x[0]))
#         h1_size = sorted_fonts[0][0] if sorted_fonts else 12.0
#         h2_size = sorted_fonts[1][0] if len(sorted_fonts) > 1 else h1_size - 1
#
#         # Create final outline
#         for item in all_text_lines:
#             level = "H1" if item["font_size"] >= h1_size else "H2"
#             outline.append({
#                 "level": level,
#                 "text": item["text"],
#                 "page": item["page"]
#             })
#
#         title = outline[0]["text"] if outline else os.path.basename(file_path)
#
#     return {
#         "title": title,
#         "outline": outline
#     }
#
# # Docker-compatible I/O block
# input_dir = "/app/input"
# output_dir = "/app/output"
#
# for filename in os.listdir(input_dir):
#     if filename.lower().endswith(".pdf"):
#         filepath = os.path.join(input_dir, filename)
#         result = extract_outline_from_pdf(filepath)
#
#         output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)
#
#         print(f"✅ Processed: {filename}")

################################################################################################

# import os
# import json
# import pdfplumber
# from collections import defaultdict
# import re
#
# def is_bold(fontname):
#     return fontname and any(weight in fontname.lower() for weight in ["bold", "bd", "black"])
#
# def is_valid_heading(text):
#     if not text or len(text.strip()) < 4:
#         return False
#     if re.match(r"^\d+$", text.strip()):
#         return False
#     if "@" in text or re.search(r"\.com|\.(org|edu|net)", text):
#         return False
#     return True
#
# def extract_outline_from_pdf(file_path):
#     outline = []
#     font_counter = defaultdict(int)
#     text_blocks = []
#
#     with pdfplumber.open(file_path) as pdf:
#         for page_num, page in enumerate(pdf.pages, 1):
#             for char in page.chars:
#                 text = char.get("text", "").strip()
#                 fontname = char.get("fontname", "").lower()
#                 font_size = round(char.get("size", 0), 1)
#                 x0 = round(char.get("x0", 0), 1)
#                 top = round(char.get("top", 0), 1)
#
#                 if not text:
#                     continue
#
#                 text_blocks.append({
#                     "text": text,
#                     "size": font_size,
#                     "fontname": fontname,
#                     "x0": x0,
#                     "top": top,
#                     "page": page_num
#                 })
#
#     # Group text by page and line (top ~ line)
#     grouped_lines = defaultdict(list)
#     for block in text_blocks:
#         key = (block["page"], round(block["top"] / 2) * 2)
#         grouped_lines[key].append(block)
#
#     lines = []
#     for (page, top), group in grouped_lines.items():
#         group_sorted = sorted(group, key=lambda x: x["x0"])
#         line_text = "".join([w["text"] for w in group_sorted]).strip()
#         if not is_valid_heading(line_text):
#             continue
#
#         size = group_sorted[0].get("size", 0)
#         fontname = group_sorted[0].get("fontname", "")
#
#         if is_bold(fontname):
#             lines.append({
#                 "text": line_text,
#                 "size": size,
#                 "fontname": fontname,
#                 "page": page
#             })
#             font_counter[size] += 1
#
#     # Determine H1 and H2 thresholds
#     sorted_fonts = sorted(font_counter.items(), key=lambda x: (-x[1], -x[0]))
#     h1_size = sorted_fonts[0][0] if sorted_fonts else 14.0
#     h2_size = sorted_fonts[1][0] if len(sorted_fonts) > 1 else h1_size - 1
#
#     for line in lines:
#         level = "H1" if line["size"] >= h1_size else "H2" if line["size"] >= h2_size else None
#         if level:
#             outline.append({
#                 "level": level,
#                 "text": line["text"],
#                 "page": line["page"]
#             })
#
#     title = outline[0]["text"] if outline else os.path.basename(file_path)
#     return {
#         "title": title,
#         "outline": outline
#     }
#
# # --- Docker paths ---
# input_dir = "/app/input"
# output_dir = "/app/output"
#
# for filename in os.listdir(input_dir):
#     if filename.lower().endswith(".pdf"):
#         filepath = os.path.join(input_dir, filename)
#         try:
#             result = extract_outline_from_pdf(filepath)
#             out_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
#             with open(out_path, "w", encoding="utf-8") as f:
#                 json.dump(result, f, indent=2, ensure_ascii=False)
#             print(f"✅ Processed: {filename}")
#         except Exception as e:
#             print(f"❌ Failed: {filename} | Error: {e}")

################################################################################################################3

import os
import json
import pdfplumber
from collections import defaultdict
import re

# --- Utility Functions ---

def is_bold(fontname):
    return fontname and any(weight in fontname.lower() for weight in ["bold", "bd", "black"])

def is_valid_heading(text):
    if not text or len(text.strip()) < 4:
        return False
    if re.match(r"^\d+$", text.strip()):
        return False
    if "@" in text or re.search(r"\.com|\.(org|edu|net)", text):
        return False
    return True

def prettify_heading(text):
    # Add spacing between glued words and handle numeric-word boundaries
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', text)
    text = re.sub(r'([a-z])([A-Z0-9])', r'\1 \2', text)
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)
    text = re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', text)
    text = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# --- Core Outline Extraction ---

def extract_outline_from_pdf(file_path):
    outline = []
    font_counter = defaultdict(int)
    text_blocks = []

    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            for char in page.chars:
                text = char.get("text", "").strip()
                fontname = char.get("fontname", "").lower()
                font_size = round(char.get("size", 0), 1)
                x0 = round(char.get("x0", 0), 1)
                top = round(char.get("top", 0), 1)

                if not text:
                    continue

                text_blocks.append({
                    "text": text,
                    "size": font_size,
                    "fontname": fontname,
                    "x0": x0,
                    "top": top,
                    "page": page_num
                })

    # Group text by (page, line_top)
    grouped_lines = defaultdict(list)
    for block in text_blocks:
        key = (block["page"], round(block["top"] / 2) * 2)
        grouped_lines[key].append(block)

    lines = []
    for (page, top), group in grouped_lines.items():
        group_sorted = sorted(group, key=lambda x: x["x0"])
        line_text = "".join([w["text"] for w in group_sorted]).strip()
        if not is_valid_heading(line_text):
            continue

        size = group_sorted[0].get("size", 0)
        fontname = group_sorted[0].get("fontname", "")

        if is_bold(fontname):
            lines.append({
                "text": line_text,
                "size": size,
                "fontname": fontname,
                "page": page
            })
            font_counter[size] += 1

    # Heading size thresholds
    sorted_fonts = sorted(font_counter.items(), key=lambda x: (-x[1], -x[0]))
    h1_size = sorted_fonts[0][0] if sorted_fonts else 14.0
    h2_size = sorted_fonts[1][0] if len(sorted_fonts) > 1 else h1_size - 1

    for line in lines:
        level = "H1" if line["size"] >= h1_size else "H2" if line["size"] >= h2_size else None
        if level:
            outline.append({
                "level": level,
                "text": prettify_heading(line["text"]),
                "page": line["page"]
            })

    title = outline[0]["text"] if outline else os.path.basename(file_path)
    return {
        "title": prettify_heading(title),
        "outline": outline
    }

# --- File System Integration (Docker compatible) ---

input_dir = "/app/input"
output_dir = "/app/output"

for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        filepath = os.path.join(input_dir, filename)
        try:
            result = extract_outline_from_pdf(filepath)
            out_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ Processed: {filename}")
        except Exception as e:
            print(f"❌ Failed: {filename} | Error: {e}")




