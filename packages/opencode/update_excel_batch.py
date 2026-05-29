
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

    # Convert list of dictionaries to a DataFrame
    new_records_df = pd.DataFrame(records)
    
    # Concatenate the existing DataFrame with the new records
    df = pd.concat([df, new_records_df], ignore_index=True)

    # Ensure all columns are present and in the correct order
    df = df.reindex(columns=all_columns)

    df.to_excel(file_path, index=False)
    print(f"Successfully appended {len(records)} new records to {file_path}.")

def main():
    excel_file = r"C:\Users\winst\OneDrive\Winston ArcSage\Agent Skills\opencode\opencode_tax_receipts.xlsx"

    new_receipts = [
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\Claude\Receipt-2181-0433-0435.pdf",
            "Date": "2026-01-03",
            "Vendor": "Anthropic, PBC",
            "Total Amount": 34.00,
            "GST": 3.09,
            "Description": "Claude Pro",
            "Invoice Number": "QI8J7X4U-0009",
            "Receipt Number": "2181-0433-0435",
            "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\Claude\Receipt-2557-3607-2169.pdf",
            "Date": "2025-11-15",
            "Vendor": "Anthropic, PBC",
            "Total Amount": 136.05,
            "GST": 12.36,
            "Description": "Max plan - 5x, Unused time on Claude Pro",
            "Invoice Number": "QI8J7X4U-0002",
            "Receipt Number": "2557-3607-2169",
            "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\Claude\Receipt-2650-1454-7215.pdf",
            "Date": "2026-01-04",
            "Vendor": "Anthropic, PBC",
            "Total Amount": 137.25,
            "GST": 12.47,
            "Description": "Max plan - 5x, Unused time on Claude Pro",
            "Invoice Number": "QI8J7X4U-0010",
            "Receipt Number": "2650-1454-7215",
            "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\Claude\Receipt-2907-2221-7125.pdf",
            "Date": "2025-11-21",
            "Vendor": "Anthropic, PBC",
            "Total Amount": 34.00,
            "GST": 3.09,
            "Description": "Claude Pro",
            "Invoice Number": "QI8J7X4U-0003",
            "Receipt Number": "2907-2221-7125",
            "Category": "AI Services"
        },
        {
            "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\Claude\Refund-3037-0426.pdf",
            "Date": "2025-11-16",
            "Vendor": "Anthropic, PBC",
            "Total Amount": -136.05,
            "GST": -12.36,
            "Description": "Refund for Max plan & Unused time",
            "Invoice Number": "QI8J7X4U-0002",
            "Receipt Number": "Refund",
            "Category": "AI Services"
        }
    ]

    append_to_excel(excel_file, new_receipts)

if __name__ == "__main__":
    main()
