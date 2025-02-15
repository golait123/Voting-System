from db_connection import get_connection
from biometric import wait_for_fingerprint, get_aadhar_biometric, verify_biometric


def validate_voter(voter_id, aadhar_id, scanner_choice):
    """
    Validates the voter by:
      1. Checking the database for matching voter details and ensuring they haven't voted.
      2. Waiting for fingerprint input on the selected scanner (A or B).
      3. Fetching the official biometric hash for the provided Aadhar ID from a CSV file.
      4. Verifying the scanned fingerprint hash against the stored biometric hash.

    Returns True if all checks pass; otherwise, False.
    """
    # Step 1: Validate voter details from the database.
    conn = get_connection()
    if conn is None:
        print("Database connection error!")
        return False
    cursor = conn.cursor()
    sql = "SELECT aadhar_id, has_voted FROM voters WHERE voter_id = %s"
    cursor.execute(sql, (voter_id,))
    result = cursor.fetchone()
    if result is None:
        print("Voter not found!")
        conn.close()
        return False
    db_aadhar, has_voted = result
    if db_aadhar != aadhar_id:
        print("Aadhar number does not match!")
        conn.close()
        return False
    if has_voted == 1:
        print("This voter has already cast a vote!")
        conn.close()
        return False
    conn.close()

    # Step 2: Wait for fingerprint input using the selected scanner.
    scanned_hash = wait_for_fingerprint(scanner_choice)
    if scanned_hash is None:
        print("Fingerprint scan aborted.")
        return False

    # Step 3: Retrieve the stored biometric hash from the CSV file.
    stored_hash = get_aadhar_biometric(aadhar_id)
    if stored_hash is None:
        print("Stored biometric data for the provided Aadhar ID not found.")
        return False

    # Step 4: Verify the scanned fingerprint.
    if not verify_biometric(scanned_hash, stored_hash):
        print("Fingerprint authentication failed!")
        return False

    return True


def get_candidate_id_by_party(party_name):
    """
    Retrieves the candidate (party) ID from the candidates table based on the party name.
    """
    conn = get_connection()
    if conn is None:
        print("Database connection error!")
        return None
    cursor = conn.cursor()
    sql = "SELECT candidate_id FROM candidates WHERE party_name = %s"
    cursor.execute(sql, (party_name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


def cast_vote(voter_id, candidate_id):
    """
    Records the vote in the votes table, increments the candidate's vote count,
    and marks the voter as having voted.
    """
    conn = get_connection()
    if conn is None:
        print("Database connection error!")
        return
    cursor = conn.cursor()
    try:
        sql_vote = "INSERT INTO votes (voter_id, candidate_id) VALUES (%s, %s)"
        cursor.execute(sql_vote, (voter_id, candidate_id))

        sql_update_candidate = "UPDATE candidates SET vote_count = vote_count + 1 WHERE candidate_id = %s"
        cursor.execute(sql_update_candidate, (candidate_id,))

        sql_update_voter = "UPDATE voters SET has_voted = 1 WHERE voter_id = %s"
        cursor.execute(sql_update_voter, (voter_id,))

        conn.commit()
        print("Vote cast successfully!")
    except Exception as e:
        conn.rollback()
        print("An error occurred while casting the vote:", e)
    finally:
        conn.close()


def get_live_results():
    """
    Retrieves live vote counts for each party from the candidates table.
    Returns a list of tuples (party_name, vote_count).
    """
    conn = get_connection()
    if conn is None:
        print("Database connection error!")
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT party_name, vote_count FROM candidates")
    results = cursor.fetchall()
    conn.close()
    return results


def voting_session():
    """
    Runs the complete voting session:
      - Prompts for Voter ID and Aadhar number.
      - Activates both fingerprint scanners (A and B) for Party A and Party B.
      - The voter selects which scanner they are using.
      - The system validates voter details and waits for the fingerprint input.
      - If authentication succeeds, the vote is cast for the corresponding party.
    """
    print("Welcome to the Electronic Voting System")
    voter_id = input("Enter your Voter ID: ").strip()
    aadhar_id = input("Enter your Aadhar number: ").strip()

    print("\nTwo fingerprint scanners are active:")
    print("Scanner A is for Party A.")
    print("Scanner B is for Party B.")
    scanner_choice = input("Which scanner are you using? (Enter A or B): ").strip().upper()

    if scanner_choice not in ['A', 'B']:
        print("Invalid scanner choice. Exiting.")
        return

    # Validate voter details and biometric data.
    if not validate_voter(voter_id, aadhar_id, scanner_choice):
        print("Voter validation failed. Exiting.")
        return
    print("Voter validated successfully!")

    # Determine the party based on the scanner used.
    party_name = "Party A" if scanner_choice == 'A' else "Party B"
    print(f"Your vote will be cast for {party_name}.")

    candidate_id = get_candidate_id_by_party(party_name)
    if candidate_id is None:
        print("Candidate not found for the chosen party!")
        return

    cast_vote(voter_id, candidate_id)


if __name__ == "__main__":
    voting_session()
