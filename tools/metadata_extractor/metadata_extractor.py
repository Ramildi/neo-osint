#!/usr/bin/env python3
# METADATA EXTRACTOR – OSINT TOOL
# Legal use only

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import PyPDF2
import docx
import sys
import json
from pathlib import Path

# ================= IMAGE METADATA ================= #

def extract_image_metadata(file_path):
    data = {}
    try:
        img = Image.open(file_path)
        exifdata = img._getexif()

        if not exifdata:
            return {"info": "No EXIF metadata found"}

        for tag_id, value in exifdata.items():
            tag = TAGS.get(tag_id, tag_id)
            data[tag] = value

        return data
    except Exception as e:
        return {"error": str(e)}

# ================= PDF METADATA ================= #

def extract_pdf_metadata(file_path):
    data = {}
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            meta = reader.metadata

            if meta:
                for key, value in meta.items():
                    data[key.replace("/", "")] = value
            else:
                data["info"] = "No metadata found"

        return data
    except Exception as e:
        return {"error": str(e)}

# ================= DOCX METADATA ================= #

def extract_docx_metadata(file_path):
    data = {}
    try:
        doc = docx.Document(file_path)
        props = doc.core_properties

        data = {
            "author": props.author,
            "last_modified_by": props.last_modified_by,
            "created": str(props.created),
            "modified": str(props.modified),
            "title": props.title,
            "subject": props.subject,
            "keywords": props.keywords
        }
        return data
    except Exception as e:
        return {"error": str(e)}

# ================= MAIN ENGINE ================= #

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <file>")
        sys.exit(1)

    file_path = sys.argv[1]
    file = Path(file_path)

    if not file.exists():
        print("File not found!")
        sys.exit(1)

    print("\n[ METADATA EXTRACTION STARTED ]\n")

    result = {
        "file": str(file),
        "type": file.suffix.lower(),
        "metadata": {}
    }

    if file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        result["metadata"] = extract_image_metadata(file)

    elif file.suffix.lower() == ".pdf":
        result["metadata"] = extract_pdf_metadata(file)

    elif file.suffix.lower() == ".docx":
        result["metadata"] = extract_docx_metadata(file)

    else:
        print("Unsupported file type")
        sys.exit(1)

    print(json.dumps(result, indent=4, ensure_ascii=False))

    with open(f"metadata_{file.stem}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"\n📁 Output saved: metadata_{file.stem}.json\n")

if __name__ == "__main__":
    main()
