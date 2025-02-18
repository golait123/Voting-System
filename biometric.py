import csv
import hashlib


def wait_for_fingerprint(scanner_label):
    """
    Waits until the voter places their finger on the designated scanner.
    Returns the SHA256 hash of the input fingerprint data, or None if aborted.
    """
    print(f"Waiting for fingerprint input on Scanner {scanner_label}...")
    while True:
        fingerprint_input = input(f"Place your finger on Scanner {scanner_label} (or type 'cancel' to abort): ")
        if fingerprint_input.lower() == 'cancel':
            return None
        if fingerprint_input.strip():
            # Fingerprint data received: return its SHA256 hash.
            return hashlib.sha256(fingerprint_input.encode()).hexdigest()
        else:
            print("No fingerprint detected. Please try again.")


def get_aadhar_biometric(aadhar_id, file_path="aadhar_biometrics.csv"):
    """
    Reads the CSV file to retrieve the stored biometric hash for a given Aadhar ID.
    The CSV file must have a header with columns "aadhar_id" and "biometric_hash".

    Returns the biometric hash if found, or None otherwise.
    """
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader("Book1.csv")
            for row in reader:
                if row["aadhar_id"].strip() == aadhar_id:
                    return row["biometric_hash"].strip()
    except FileNotFoundError:
        print(f"CSV file {file_path} not found.")
    except Exception as e:
        print("Error reading CSV file:", e)
    return None


def verify_biometric(scanned_hash, stored_hash):
    """
    Compares the scanned fingerprint hash with the stored biometric hash.
    Returns True if they match, False otherwise.
    """
    return scanned_hash == stored_hash
