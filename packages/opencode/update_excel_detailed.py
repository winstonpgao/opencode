
import pandas as pd
import os

def update_excel_with_details(file_path, new_data):
    """
    Reads an existing Excel file, adds new data with more details, and saves it.
    If the file doesn't exist, it creates a new one with the correct columns.
    """
    
    # Define all columns to ensure consistency
    all_columns = [
        "File Path", "Date", "Vendor", "Total Amount", "GST", 
        "Description", "Invoice Number", "Receipt Number", "Category"
    ]

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=all_columns)

    # Ensure all columns are present, adding any that are missing
    for col in all_columns:
        if col not in df.columns:
            df[col] = None # Add missing column with default value

    # Append new data as a new DataFrame
    new_df = pd.DataFrame([new_data])
    df = pd.concat([df, new_df], ignore_index=True)

    # Reorder columns to the desired format
    df = df[all_columns]

    # Save the updated dataframe
    df.to_excel(file_path, index=False)
    print(f"Successfully updated {file_path} with new detailed data.")

def main():
    excel_file = r"C:\Users\winst\OneDrive\Winston ArcSage\Agent Skills\opencode\opencode_tax_receipts.xlsx"

    # Data extracted from the first PDF including new details
    new_receipt_data = {
        "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\Claude\Receipt-2089-7255-9892.pdf",
        "Date": "2025-11-25",
        "Vendor": "Anthropic, PBC",
        "Total Amount": 139.60,
        "GST": 12.69,
        "Description": "Max plan - 5x, Unused time on Claude Pro",
        "Invoice Number": "QI8J7X4U-0005",
        "Receipt Number": "2089-7255-9892",
        "Category": "AI Services"
    }

    update_excel_with_details(excel_file, new_receipt_data)

if __name__ == "__main__":
    main()
