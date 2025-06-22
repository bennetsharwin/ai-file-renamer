# Smart File Renamer (GenAI‑Powered)

**Smart File Renamer** is an intelligent, AI-powered Python tool that automatically analyzes image and document content to generate meaningful and structured filenames. It transforms cryptic names like `IMG_1234.jpg` into descriptive names such as `2025-06-10_coffee_receipt.jpg`, enhancing searchability, organization, and productivity.

---

## 🚀 Features

- **AI-Powered Image Analysis**  
  Utilizes Google Gemini Vision to identify objects, scenes, and text in images—supports screenshots, receipts, photos, diagrams, etc.

- **Document Content Parsing**  
  Employs OCR and NLP to extract topics and dates from PDFs, text files, and code—produces names like `Invoice_Apple_2025_Q1.pdf`.

- **Metadata & EXIF Support**  
  Extracts EXIF dates from images; falls back to file metadata and inferred dates via content when necessary.

- **Safe, Consistent Filenames**  
  Formats in snake_case with optional PascalCase, strips invalid symbols, and detects filename conflicts.

- **Batch Processing & Recursion**  
  Recursively scans directories, supports dry-run preview mode, and logs all renaming actions.

---

## 🧠 Why Use It

- Automates monotonous renaming tasks for photographers, researchers, accountants, and developers.  
- Produces structured, human-readable filenames that make file retrieval intuitive.  
- Fits seamlessly into automated workflows and can be customized with templates.

---

## ⚙️ Installation

```sh
git clone https://github.com/yourusername/smart-file-renamer.git
cd smart-file-renamer
pip install -r requirements.txt
