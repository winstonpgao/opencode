
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

    bizcover_receipts = [
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\BizCover\invoice-10119344-20-20251223103038.pdf",
            "Date": "2025-12-23", "Vendor": "BizCover Pty Ltd", "Total Amount": 414.48, "GST": 36.00,
            "Description": "Professional Indemnity & Public Liability Insurance", "Invoice Number": "10119344-20", "Category": "Insurance"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\BizCover\payment-schedule-10119344-20251223103032.pdf",
            "Date": "2025-12-23", "Vendor": "BizCover Pty Ltd", "Total Amount": 43.77, "GST": 3.84,
            "Description": "Monthly Instalment for Insurance", "Invoice Number": "10119344_0", "Category": "Insurance"
        }
    ]

    append_to_excel(excel_file, bizcover_receipts)

if __name__ == "__main__":
    main()
