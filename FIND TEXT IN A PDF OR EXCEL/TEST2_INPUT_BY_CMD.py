import os
import sys
import warnings
import pandas as pd
import pdfplumber

# Mute openpyxl warnings to keep the screen clean
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

print("=============================================")
print("     📂 LOCAL EXCEL & PDF SEARCH TOOL        ")
print("=============================================\n")

# 1. Ask user for the folder path
FOLDER_PATH = input("👉 Enter or paste the full folder path: ").strip()

# Clean up quotes if the user dragged and dropped the folder into CMD
FOLDER_PATH = FOLDER_PATH.strip('"').strip("'")

# Validate the path
if not os.path.exists(FOLDER_PATH):
    print(f"\n❌ Error: The folder path '{FOLDER_PATH}' does not exist.")
    input("\nPress Enter to exit...")
    sys.exit(1)

# 2. Ask user for the text to search
RAW_SEARCH_TEXT = input("👉 Enter the text you want to find: ").strip()
SEARCH_TEXT = RAW_SEARCH_TEXT.lower()

if not SEARCH_TEXT:
    print("\n❌ Error: Search text cannot be empty.")
    input("\nPress Enter to exit...")
    sys.exit(1)

print(f"\n🔍 Searching for '{RAW_SEARCH_TEXT}'... please wait...\n")
found_count = 0

for root, dirs, files in os.walk(FOLDER_PATH):
    for file in files:
        file_path = os.path.join(root, file)
        
        # --- SEARCH IN EXCEL FILES ---
        if file.endswith(('.xlsx', '.xls', '.csv')):
            try:
                excel_file = pd.ExcelFile(file_path)
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name).astype(str)
                    if df.stack().str.lower().str.contains(SEARCH_TEXT).any():
                        print(f"[FOUND IN EXCEL] Sheet '{sheet_name}': {file_path}")
                        found_count += 1
            except BaseException:
                pass
                
        # --- SEARCH IN PDF FILES ---
        elif file.endswith('.pdf'):
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text and SEARCH_TEXT in text.lower():
                            print(f"[FOUND IN PDF] Page {page_num + 1}: {file_path}")
                            found_count += 1
                            break
            except BaseException:
                pass

print(f"\n✨ Search complete! Found matches in {found_count} files.")
# Keeps the window open so you can read the results
input("\nPress Enter to exit...")