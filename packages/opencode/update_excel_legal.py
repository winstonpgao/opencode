
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

    legal_receipts = [
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\Legal Fees\Lawdepot 17 Nov 2025.pdf",
            "Date": "2025-11-17", "Vendor": "LawDepot", "Total Amount": 39.00, "GST": 3.55,
            "Description": "Trial Site Subscription Renewal", "Invoice Number": "LWS-111625-080530-945", "Category": "Legal Fees"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\Legal Fees\Lawdepot 26 Sep 2025.pdf",
            "Date": "2025-09-26", "Vendor": "LawDepot", "Total Amount": 39.00, "GST": 3.55,
            "Description": "Trial Site Subscription Renewal", "Invoice Number": "LWS-092625-040818-619", "Category": "Legal Fees"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\Legal Fees\Lawpath Business Name.pdf",
            "Date": "2025-03-15", "Vendor": "Lawpath", "Total Amount": 211.65, "GST": 9.73,
            "Description": "Business name (3 year)", "Invoice Number": "7306443788585533440", "Category": "Legal Fees"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\Legal Fees\Lawpath Company Registration.pdf",
            "Date": "2025-03-09", "Vendor": "Lawpath", "Total Amount": 784.81, "GST": 17.07,
            "Description": "Company Registration, Document Compliance, Tax Compliance", "Invoice Number": "7304356603954724864", "Category": "Legal Fees"
        }
    ]

    append_to_excel(excel_file, legal_receipts)

if __name__ == "__main__":
    main()
