#transaction log reader
import sys

def load_transactions(filename="telebirr transactions.txt"):
    """
    Reads transactions from a text file and returns a dictionary 
    containing the total amount spent per customer.
    """
    customer_totals = {}

    try:
        # Open the file in read-only mode
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                # Clean up hidden whitespace and newlines
                clean_line = line.strip()
                
                # Skip empty lines cleanly
                if not clean_line:
                    continue
                
                try:
                    # Split the line into Customer Name and Transaction Amount
                    customer, amount_str = clean_line.split(",")
                    amount = float(amount_str)
                    
                    # Update or insert the data into our dictionary
                    if customer in customer_totals:
                        customer_totals[customer] += amount
                    else:
                        customer_totals[customer] = amount
                        
                except ValueError:
                    print(f"[-] Warning: Skipping malformed data on line {line_number}: '{clean_line}'")
                    continue

        return customer_totals

    except FileNotFoundError:
        print(f"\n[-] Critical Error: The file '{filename}' could not be located.")
        print("[*] Troubleshooting steps:")
        print("    1. Ensure the file exists in the exact same folder as this script.")
        print("    2. Verify the filename is spelled correctly.\n")
        # Return None to indicate the operation failed gracefully
        return None

def display_summary(totals_dict):
    """
    Displays the final calculated balances in a clean, professional dashboard.
    """
    if totals_dict is None:
        print("[-] Execution halted: No data available to summarize.")
        return

    if not totals_dict:
        print("[!] Execution note: The transaction log file was empty.")
        return

    print("\n" + "=" * 50)
    print("📱 TELEBIRR CUSTOMER TRANSACTION SUMMARY")
    print("=" * 50)
    
    # Sort the summary by customer name for clean tracking
    for customer, total_balance in sorted(totals_dict.items()):
        print(f"  👤 Customer: {customer:<12} | 💰 Total: {total_balance:,.2f} Birr")
        
    print("=" * 50)
    print("[✓] Processing complete.\n")

if __name__ == "__main__":
    # Define the target transaction file
    TARGET_FILE = "telebirr transactions.txt"
    
    # Run the core logic pipeline
    processed_data = load_transactions(TARGET_FILE)
    display_summary(processed_data)