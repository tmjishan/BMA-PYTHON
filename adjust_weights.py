import xlwings as xw
import tkinter as tk
from tkinter import simpledialog, messagebox

@xw.sub
def main():
    wb = xw.books.active
    
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    # 1. Sheet prefixes input box
    prefix_input = simpledialog.askstring(
        "Filter Sheet Prefixes", 
        "Enter sheet name prefixes (comma separated):\n(e.g., FV, FGI, T):"
    )
    
    if prefix_input is None:
        root.destroy()
        return
        
    prefixes = [p.strip().upper() for p in prefix_input.split(',') if p.strip()]
    
    if not prefixes:
        messagebox.showerror("Error", "Apnake at least ekta prefix ditei hobe!")
        root.destroy()
        return

    # 2. Gross Weight (AC Column) adjustment value per carton
    gw_input = simpledialog.askstring(
        "Gross Weight Adjustment (AC)", 
        "Enter Gross Weight adjustment value per carton:\n(e.g., 0.5 for plus, -0.5 for minus):"
    )
    
    if gw_input is None:
        root.destroy()
        return

    # 3. CBM (Z Column) adjustment value per carton
    cbm_input = simpledialog.askstring(
        "CBM Adjustment (Z)", 
        "Enter CBM adjustment value per carton:\n(e.g., 0.001 for plus, -0.001 for minus):"
    )
    
    if cbm_input is None:
        root.destroy()
        return

    def parse_input(val_str):
        if not val_str or val_str.strip() == "":
            return 0.0, False
        val_str = val_str.strip()
        is_minus = False
        if val_str.startswith('-'):
            is_minus = True
            v = val_str[1:].strip()
        elif val_str.startswith('+'):
            is_minus = False
            v = val_str[1:].strip()
        else:
            v = val_str
        return float(v), is_minus

    try:
        gw_val, gw_minus = parse_input(gw_input)
        c_val, c_minus = parse_input(cbm_input)
    except ValueError:
        messagebox.showerror("Error", "Sothik numeric value din!")
        root.destroy()
        return

    updated_sheets_count = 0

    for sheet in wb.sheets:
        if not sheet.visible:
            continue
            
        sheet_name_upper = sheet.name.strip().upper()
        matches_prefix = any(sheet_name_upper.startswith(pref) for pref in prefixes)
        
        if not matches_prefix:
            continue
            
        updated_sheets_count += 1
        
        col_a = sheet.range("A10:A500").value
        total_row = None
        
        if col_a:
            for idx, val in enumerate(col_a, start=10):
                if val is not None and str(val).strip().upper() in ["TOTAL=", "TOTAL"]:
                    total_row = idx
                    break
                    
        if not total_row:
            continue
            
        for r in range(10, total_row):
            # --- Gross Weight (AC Column) Calculation ---
            if gw_val != 0.0:
                cell = sheet.range(f"AC{r}")
                formula = cell.formula
                
                if formula and str(formula).startswith('='):
                    formula_body = formula[1:]
                    if gw_minus:
                        cell.formula = f"=({formula_body})-({gw_val}*T{r})"
                    else:
                        cell.formula = f"=({formula_body})+({gw_val}*T{r})"
                else:
                    val = cell.value
                    if val is not None:
                        try:
                            num = float(val)
                            if gw_minus:
                                cell.formula = f"={num}-({gw_val}*T{r})"
                            else:
                                cell.formula = f"={num}+({gw_val}*T{r})"
                        except ValueError:
                            pass

            # --- CBM (Z Column) Calculation ---
            if c_val != 0.0:
                cell = sheet.range(f"Z{r}")
                formula = cell.formula
                
                if formula and str(formula).startswith('='):
                    formula_body = formula[1:]
                    # Fixed bracket syntax error here:
                    if c_minus:
                        cell.formula = f"=({formula_body})-({c_val}*T{r})"
                    else:
                        cell.formula = f"=({formula_body})+({c_val}*T{r})"
                else:
                    val = cell.value
                    if val is not None:
                        try:
                            num = float(val)
                            if c_minus:
                                cell.formula = f"={num}-({c_val}*T{r})"
                            else:
                                cell.formula = f"={num}+({c_val}*T{r})"
                        except ValueError:
                            pass

    root.destroy()
    messagebox.showinfo("Success", f"Successfully {updated_sheets_count} ta sheet update kora hoyeche!")