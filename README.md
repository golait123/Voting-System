Electronic Voting System with Fingerprint Authentication
Overview
This project is a Python-based electronic voting system that leverages biometric fingerprint scanning for secure voter authentication. The system uses two dedicated fingerprint scanners—Scanner A for Party A and Scanner B for Party B. Depending on which scanner the voter uses, the vote is automatically cast for the corresponding party.

The application connects to a PostgreSQL database to store voter, candidate, and vote records, and it uses a CSV file (aadhar_biometrics.csv) to retrieve Aadhar biometric details for fingerprint verification. A Tkinter-based GUI displays real-time voting results.

Features
Biometric Fingerprint Authentication:
Captures a fingerprint from a dedicated scanner and converts it into a SHA256 hash.

Dual Scanner Voting:

Scanner A: Votes for Party A
Scanner B: Votes for Party B
CSV-based Biometric Data:
Retrieves stored biometric hashes for Aadhar IDs from a CSV file with headers aadhar_id and biometric_hash.

Database Integration:
Uses PostgreSQL to store:

Voters: (voter_id, aadhar_id, fingerprint_hash, has_voted)
Candidates: (candidate_id, party_name, vote_count)
Votes: (vote_id, voter_id, candidate_id, vote_time)
Real-Time Results GUI:
A Tkinter interface shows live vote counts, updating at regular intervals.

Project Structure
bash
Copy
Edit
VotingSystem/
├── db_connection.py        # Handles connection to the PostgreSQL database.
├── biometric.py            # Contains functions for fingerprint capture and verification using CSV data.
├── voting.py               # Implements voter validation, vote casting, and result retrieval.
├── live_results_gui.py     # Tkinter GUI to display real-time voting results.
└── main.py                 # Main entry point for the voting system.
Setup Instructions
1. Database Setup in PostgreSQL
Using pgAdmin or psql, create the required tables in your PostgreSQL database (e.g., using the default database postgres):

sql
Copy
Edit
-- Create voters table
CREATE TABLE voters (
    voter_id VARCHAR(20) PRIMARY KEY,
    aadhar_id VARCHAR(20) NOT NULL,
    fingerprint_hash CHAR(64),
    has_voted SMALLINT DEFAULT 0
);

-- Create candidates table
CREATE TABLE candidates (
    candidate_id SERIAL PRIMARY KEY,
    party_name VARCHAR(50) NOT NULL,
    vote_count INT DEFAULT 0
);

-- Create votes table
CREATE TABLE votes (
    vote_id SERIAL PRIMARY KEY,
    voter_id VARCHAR(20) REFERENCES voters(voter_id),
    candidate_id INT REFERENCES candidates(candidate_id),
    vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample candidates
INSERT INTO candidates (party_name, vote_count) VALUES ('Party A', 0);
INSERT INTO candidates (party_name, vote_count) VALUES ('Party B', 0);
2. CSV File Setup
Create a CSV file named aadhar_biometrics.csv in the project directory with the following format:

csv
Copy
Edit
aadhar_id,biometric_hash
AADHAR123,9a0364b9e99bb480dd25e1f0284c8555
AADHAR456,5d41402abc4b2a76b9719d911017c592
Note: Replace the hash values with the actual SHA256 hashes of the registered fingerprint codes.

3. Python Environment
Create a virtual environment:
bash
Copy
Edit
python -m venv .venv
Activate the virtual environment and install dependencies:
bash
Copy
Edit
pip install psycopg2-binary
4. Running the Project
To launch the voting session or view live results, run:
bash
Copy
Edit
python main.py
Follow the on-screen prompts:
Enter your voter ID and Aadhar number.
Choose the fingerprint scanner (A or B) to vote for the corresponding party.
The system will wait for your fingerprint input, verify it against the CSV data, and cast your vote if authenticated.
Alternatively, select the live results interface to view current vote counts.
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for improvements, bug fixes, or new features.

License
This project is licensed under the MIT License.

Acknowledgements
Thanks to the PostgreSQL and Tkinter communities.
Inspired by the need for secure and transparent digital voting solutions
