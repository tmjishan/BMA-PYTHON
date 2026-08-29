import os
import sys
import warnings
from datetime import datetime
import pandas as pd
import pdfplumber

# Mute openpyxl warnings to keep the screen clean
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

print("=============================================")
print("  📂 SEARCH & EXPORT TO EXCEL TOOL           ")
print("=============================================\n")

# 1. Ask user for the folder path to scan
FOLDER_PATH = input("👉 Enter or paste the folder path to search: ").strip()
FOLDER_PATH = FOLDER_PATH.strip('"').strip("'")

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

# List to collect our results
results_list = []

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
                        print(f"[FOUND] Excel Sheet '{sheet_name}': {file}")
                        results_list.append({
                            "File Type": "Excel",
                            "File Name": file,
                            "Match Location": f"Sheet: {sheet_name}",
                            "Full Path": file_path
                        })
            except BaseException:
                pass
                
        # --- SEARCH IN PDF FILES ---
        elif file.endswith('.pdf'):
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text and SEARCH_TEXT in text.lower():
                            print(f"[FOUND] PDF Page {page_num + 1}: {file}")
                            results_list.append({
                                "File Type": "PDF",
                                "File Name": file,
                                "Match Location": f"Page: {page_num + 1}",
                                "Full Path": file_path
                            })
                            break
            except BaseException:
                pass

# --- EXPORT TO EXCEL ---
if results_list:
    # Convert results list to a DataFrame
    output_df = pd.DataFrame(results_list)
    
    # Get the directory where THIS script (.py file) lives
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a clean filename using the search text
    safe_search_name = "".join(x for x in RAW_SEARCH_TEXT if x.isalnum() or x in "._- ").strip()
    output_filename = f"Search_Results_{safe_search_name}.xlsx"
    output_path = os.path.join(script_dir, output_filename)
    
    # Save the file
    output_df.to_excel(output_path, index=False)
    
    print(f"\n✨ Search complete! Found matches in {len(results_list)} files.")
    print(f"💾 Results saved successfully to:\n👉 {output_path}")
else:
    print(f"\n🤷 Search complete. No matches found for '{RAW_SEARCH_TEXT}'.")

input("\nPress Enter to exit...")