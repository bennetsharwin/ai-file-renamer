# AI File Renamer (GenAI‑Powered)

**AI File Renamer** is an intelligent, AI-powered Python tool that automatically analyzes image and document content to generate meaningful and structured filenames. It transforms cryptic names like `IMG_1234.jpg` into descriptive names such as `2025-06-10_coffee_receipt.jpg`, enhancing searchability, organization, and productivity.

---

## 🚀 Features

- **AI-Powered Image Analysis**  
  Utilizes Google Gemini Vision to identify objects, scenes, and text in images. supports screenshots, receipts, photos, diagrams, etc.

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
git clone https://github.com/yourusername/ai-file-renamer.git
cd ai-file-renamer
pip install -r requirements.txt
```

---

## 🔑 Setting Your Google Gemini API Key

Before running the tool, you must set your Google Gemini API key as an environment variable. Replace `YOUR_API_KEY_HERE` with your actual API key.

**On Windows PowerShell:**
```powershell
$env:google_api_key="YOUR_API_KEY_HERE"
```

**On Windows Command Prompt (cmd):**
```cmd
set google_api_key=YOUR_API_KEY_HERE
```

You must run the above command in the same terminal session before executing the Python script.

---

## ▶️ Running the Tool

To run the AI File Renamer, use the following command:

```sh
python main.py -s <source_folder>
```

Replace `<source_folder>` with the path to the folder containing all the images and files you want to rename. The tool will process every supported file in that folder.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions, bug reports, or want to add features, please open an issue or submit a pull request.

---