import os
import pandas as pd
from pypdf import PdfReader

# 1. Put the path to your folder here
FOLDER_PATH = r"D:\GdriveBrandbma2015" 

# 2. Put the exact text you want to find here
SEARCH_TEXT = "FRD-SS26-BMA-02C-25".lower()

print("Searching through files... please wait...")

for root, dirs, files in os.walk(FOLDER_PATH):
    for file in files:
        file_path = os.path.join(root, file)
        
        # --- SEARCH IN EXCEL FILES ---
        if file.endswith(('.xlsx', '.xls')):
            try:
                # Read all sheets in the Excel file
                excel_file = pd.ExcelFile(file_path)
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet_name).astype(str)
                    # Check if text exists anywhere in the dataframe
                    if df.stack().str.lower().str.contains(SEARCH_TEXT).any():
                        print(f"[FOUND IN EXCEL] Match in sheet '{sheet_name}': {file_path}")
            except Exception as e:
                pass # Skip broken or password-protected files
                
        # --- SEARCH IN PDF FILES ---
        elif file.endswith('.pdf'):
            try:
                reader = PdfReader(file_path)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text and SEARCH_TEXT in text.lower():
                        print(f"[FOUND IN PDF] Match on Page {page_num + 1}: {file_path}")
                        break # Found it, move to next file
            except Exception as e:
                pass

print("Search complete!")