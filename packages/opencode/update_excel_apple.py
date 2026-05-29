
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

    apple_receipts = [
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\GPT\Apple Store.pdf",
            "Date": "2026-01-05", "Vendor": "Apple (ChatGPT)", "Total Amount": 29.99, "GST": 0,
            "Description": "ChatGPT Plus Subscription", "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\GPT\Apple Store.pdf",
            "Date": "2025-11-25", "Vendor": "Apple (ChatGPT)", "Total Amount": -29.99, "GST": 0,
            "Description": "Refund for ChatGPT Plus", "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\GPT\Apple Store.pdf",
            "Date": "2025-11-23", "Vendor": "Apple (ChatGPT)", "Total Amount": -300.00, "GST": 0,
            "Description": "Refund for ChatGPT Pro", "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\GPT\Apple Store.pdf",
            "Date": "2025-11-22", "Vendor": "Apple (ChatGPT)", "Total Amount": 29.99, "GST": 0,
            "Description": "ChatGPT Plus Subscription", "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\GPT\Apple Store.pdf",
            "Date": "2025-11-02", "Vendor": "Apple (ChatGPT)", "Total Amount": 29.99, "GST": 0,
            "Description": "ChatGPT Plus Subscription", "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\GPT\Apple Store.pdf",
            "Date": "2025-12-22", "Vendor": "Apple (iCloud)", "Total Amount": 1.49, "GST": 0,
            "Description": "iCloud + 50GB storage", "Category": "Software"
        },
    ]

    append_to_excel(excel_file, apple_receipts)

if __name__ == "__main__":
    main()
