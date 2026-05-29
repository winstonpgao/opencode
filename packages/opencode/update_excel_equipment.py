
import pandas as pd
import os

def append_to_excel(file_path, records):
    """
    Appends a list of records to an Excel file.
    """
    
    all_columns = [
        "File Path", "Date", "Vendor", "Total Amount", "GST", 
        "Description", "Invoice Number", "Receipt Number", "Category"
    ]

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=all_columns)

    new_records_df = pd.DataFrame(records)
    df = pd.concat([df, new_records_df], ignore_index=True)
    df = df.reindex(columns=all_columns)
    df.to_excel(file_path, index=False)
    print(f"Successfully appended {len(records)} new records to {file_path}.")

def main():
    excel_file = r"C:\Users\winst\OneDrive\Winston ArcSage\Agent Skills\opencode\opencode_tax_receipts.xlsx"

    equipment_receipts = [
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\Equipments\emailreceipt_20250301R1801013941.pdf",
            "Date": "2025-03-01", "Vendor": "Apple Chadstone", "Total Amount": 999.00, "GST": 90.82,
            "Description": "Mac mini", "Invoice Number": "20250301R1801013941", "Category": "Equipment"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\Equipments\EmailReceipt_20251011R1801066120.pdf",
            "Date": "2025-10-11", "Vendor": "Apple Chadstone", "Total Amount": 2357.00, "GST": 214.28,
            "Description": "13-inch MacBook Air, USB-C to USB Adapter", "Invoice Number": "20251011R1801066120", "Category": "Equipment"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\Equipments\EmailReceipt_20251101R1801187882.pdf",
            "Date": "2025-11-01", "Vendor": "Apple Chadstone", "Total Amount": 5198.00, "GST": 472.54,
            "Description": "iPhone 17 Pro Max 512GB (x2)", "Invoice Number": "20251101R1801187882", "Category": "Equipment"
        }
    ]

    append_to_excel(excel_file, equipment_receipts)

if __name__ == "__main__":
    main()
