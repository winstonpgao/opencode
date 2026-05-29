
import pandas as pd

def update_excel(file_path, data_to_add):
    """
    Reads an existing Excel file, adds new data, and saves it.
    If the file doesn't exist, it creates a new one.
    """
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["File Path", "Date", "Vendor", "Total Amount", "GST", "Category"])

    # Append new data
    new_df = pd.DataFrame([data_to_add])
    df = pd.concat([df, new_df], ignore_index=True)

    # Save the updated dataframe
    df.to_excel(file_path, index=False)
    print(f"Successfully updated {file_path} with new data.")


def main():
    excel_file = r"C:\Users\winst\OneDrive\Winston ArcSage\Agent Skills\opencode\opencode_tax_receipts.xlsx"

    # Data extracted from the first PDF
    new_receipt_data = {
        "File Path": r"C:\Users\winst\OneDrive\Winston ArcSage\ArcSage Company Docs\Tax\Reciepts\AI\Claude\Receipt-2089-7255-9892.pdf",
        "Date": "2025-11-25",
        "Vendor": "Anthropic, PBC",
        "Total Amount": 139.60,
        "GST": 12.69,
        "Category": "AI Services"
    }

    update_excel(excel_file, new_receipt_data)

if __name__ == "__main__":
    main()
