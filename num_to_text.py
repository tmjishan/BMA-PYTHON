import xlwings as xw
from num2words import num2words

@xw.sub
def main(output_cell="B1"):
    wb = xw.books.active
    sheet = wb.sheets.active
    
    try:
        # ১. এক্সেলে সিলেক্ট করা সেল থেকে ভ্যালু নেওয়া
        selected_range = wb.app.selection
        val = selected_range.value
        
        # লিস্ট বা মাল্টিপল সেল হ্যান্ডেল করা
        if isinstance(val, list):
            val = val[0]
            if isinstance(val, list):
                val = val[0]
        
        # ২. ভ্যালুকে প্রোপার সংখ্যায় রূপান্তর করার ইউনিভার্সাল লজিক
        numeric_val = None
        
        if isinstance(val, (int, float)):
            numeric_val = val
        elif isinstance(val, str):
            # স্ট্রিং থেকে ডলার, কমা বা অন্য কোনো সিম্বল রিমুভ করা
            clean_val = val.replace('$', '').replace(',', '').strip()
            numeric_val = float(clean_val)
        else:
            # যদি অন্য কোনো ফরম্যাট বা অবজেক্ট হয়, তাকে স্ট্রিং বানিয়ে ট্রাই করা
            clean_val = str(val).replace('$', '').replace(',', '').strip()
            numeric_val = float(clean_val)
            
        # ৩. কনভার্শন প্রসেস
        if numeric_val is not None:
            dollars = int(numeric_val)
            # ফ্লোটিং পয়েন্ট ক্যালকুলেশন নিখুঁত রাখার জন্য round ব্যবহার করা
            cents = int(round((numeric_val - dollars) * 100))
            
            dollar_words = num2words(dollars, lang='en')
            cent_words = num2words(cents, lang='en')
            
            # কাঙ্ক্ষিত আউটপুট ফরম্যাট
            result = f"SAY - {dollar_words} dollars and {cent_words} cents only".upper()
            
            # আউটপুট সেলে বসানো
            sheet.range(output_cell).value = result
        else:
            sheet.range(output_cell).value = "Invalid Number"
            
    except Exception as e:
        # যদি কোনো এরর হয়, তবে সেলে এররের ডিটেইল দেখাবে যাতে বোঝা যায় সমস্যা কোথায়
        sheet.range(output_cell).value = f"Error: {str(e)}"