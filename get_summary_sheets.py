import xlwings as xw

@xw.sub
def main():
    wb = xw.books.active
    summary_sheet = wb.sheets.active
    
    # ১. প্রথমে V29 থেকে AA29 পর্যন্ত হেডার এবং SUM ফর্মুলাগুলো বসিয়ে দেওয়া (স্ক্রিনশট অনুযায়ী)
    summary_sheet.range("V29").value = "TOTAL="
    summary_sheet.range("W29").formula = "=SUM(W32:W65)"
    summary_sheet.range("X29").formula = "=SUM(X32:X65)"
    summary_sheet.range("Y29").formula = "=SUM(Y32:Y65)"
    summary_sheet.range("Z29").formula = "=SUM(Z32:Z65)"
    summary_sheet.range("AA29").formula = "=SUM(AA32:AA65)"
    
    # ২. স্ক্রিনশট অনুযায়ী V30 থেকে AA30 পর্যন্ত কলাম হেডারগুলো বসানো
    summary_sheet.range("V30").value = "Sheet Name"
    summary_sheet.range("W30").value = "QTY|V"
    summary_sheet.range("X30").value = "CTN.Q|T"
    summary_sheet.range("Y30").value = "NW|X"
    summary_sheet.range("Z30").value = "GW|Y"
    summary_sheet.range("AA30").value = "CBM|Z"
    
    # ৩. ডাটা রো শুরু হবে ৩২ থেকে (Row 32)
    start_row = 32
    
    for sheet in wb.sheets:
        # অ্যাক্টিভ সামারি শিট বা হিডেন শিট স্কিপ করা
        if sheet == summary_sheet or not sheet.visible:
            continue
        
        sheet_name = sheet.name
        r = start_row
        
        # V কলামে শিট নাম বসানো
        summary_sheet.range(f"V{r}").value = sheet_name
        
        # আপনার নির্দিষ্ট AGGREGATE + INDIRECT ফর্মুলাগুলো W থেকে AA কলামে বসানো
        summary_sheet.range(f"W{r}").formula = f'=IFERROR(INDIRECT("\'"&$V{r}&"\'!V"&AGGREGATE(15,6,ROW($A$1:$A$500)/(INDIRECT("\'"&$V{r}&"\'!$A$1:$A$500")="Total="),1)),"")'
        summary_sheet.range(f"X{r}").formula = f'=IFERROR(INDIRECT("\'"&$V{r}&"\'!T"&AGGREGATE(15,6,ROW($A$1:$A$500)/(INDIRECT("\'"&$V{r}&"\'!$A$1:$A$500")="Total="),1)),"")'
        summary_sheet.range(f"Y{r}").formula = f'=IFERROR(INDIRECT("\'"&$V{r}&"\'!X"&AGGREGATE(15,6,ROW($A$1:$A$500)/(INDIRECT("\'"&$V{r}&"\'!$A$1:$A$500")="Total="),1)),"")'
        summary_sheet.range(f"Z{r}").formula = f'=IFERROR(INDIRECT("\'"&$V{r}&"\'!Y"&AGGREGATE(15,6,ROW($A$1:$A$500)/(INDIRECT("\'"&$V{r}&"\'!$A$1:$A$500")="Total="),1)),"")'
        summary_sheet.range(f"AA{r}").formula = f'=IFERROR(INDIRECT("\'"&$V{r}&"\'!Z"&AGGREGATE(15,6,ROW($A$1:$A$500)/(INDIRECT("\'"&$V{r}&"\'!$A$1:$A$500")="Total="),1)),"")'
        
        start_row += 1