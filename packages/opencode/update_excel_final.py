
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

    final_receipts = [
        # Microsoft 365 Invoices
        {"File Path": "G129861379", "Date": "2025-12-14", "Vendor": "Microsoft", "Total Amount": 29.7, "GST": 2.70, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G124380165", "Date": "2025-11-14", "Vendor": "Microsoft", "Total Amount": 29.7, "GST": 2.70, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G121790527", "Date": "2025-11-05", "Vendor": "Microsoft", "Total Amount": 0.33, "GST": 0.03, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G119066604", "Date": "2025-10-14", "Vendor": "Microsoft", "Total Amount": 29.7, "GST": 2.70, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G113657913", "Date": "2025-09-14", "Vendor": "Microsoft", "Total Amount": 19.8, "GST": 1.80, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G110696524", "Date": "2025-09-05", "Vendor": "Microsoft", "Total Amount": 9.26, "GST": 0.84, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G107525947", "Date": "2025-08-14", "Vendor": "Microsoft", "Total Amount": 9.9, "GST": 0.90, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G102284053", "Date": "2025-07-14", "Vendor": "Microsoft", "Total Amount": 9.9, "GST": 0.90, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G097290805", "Date": "2025-06-14", "Vendor": "Microsoft", "Total Amount": 9.9, "GST": 0.90, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G092348635", "Date": "2025-05-14", "Vendor": "Microsoft", "Total Amount": 9.9, "GST": 0.90, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G087603485", "Date": "2025-04-14", "Vendor": "Microsoft", "Total Amount": 9.9, "GST": 0.90, "Description": "Microsoft 365", "Category": "Software"},
        {"File Path": "G082974251", "Date": "2025-03-13", "Vendor": "Microsoft", "Total Amount": 9.9, "GST": 0.90, "Description": "Microsoft 365", "Category": "Software"},
        
        # Webcentral Invoice
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\Website Domain etc\invoice-53087682-51d4-801e-98d6-c847e390921e.pdf",
            "Date": "2025-03-10", "Vendor": "Webcentral", "Total Amount": 119.40, "GST": 10.85,
            "Description": "Domain Names, Professional Email, cPanel Hosting", "Invoice Number": "W-INV-1321908", "Category": "Website Costs"
        }
    ]

    append_to_excel(excel_file, final_receipts)

if __name__ == "__main__":
    main()
