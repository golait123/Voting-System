def main():
    print("=======================================")
    print(" Welcome to the Electronic Voting System")
    print("=======================================")
    print("Please select an option:")
    print("1. Voting Session (Cast your vote)")
    print("2. Live Results Interface")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == '1':
        from voting import voting_session
        voting_session()
    elif choice == '2':
        from live_results_gui import run_live_results_gui
        run_live_results_gui()
    elif choice == '3':
        print("Exiting the system. Goodbye!")
    else:
        print("Invalid choice! Please run the program again and select a valid option.")

if __name__ == "__main__":
    main()
