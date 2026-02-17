# I confirm that AI code completion tools were disabled while writing this program.
# Name: Arja Sadhukhan
# NU ID:003163346


"""
Problem 1: Golf Scores

The Springfork Amateur Golf Club has a tournament every weekend. The club 
president has asked you to write two programs: 

• A function that will read each player's name and golf score as keyboard input, 
  then save these as records in a file named golf.txt. (Each record will have a 
  field for the player's name and a field for the player's score.)

• A function that reads the records from the golf.txt file and displays them.
"""

def write_golf_scores():
    """
    Reads player names and scores from keyboard input and saves them to golf.txt
    """
    print("\nEnter player data. Type 'done' as the player name to finish.")
    count = 0

    # "a" = append mode (keeps old records and adds new ones)
    with open("golf.txt", "a", encoding="utf-8") as file:
        while True:
            name = input("Player name: ").strip()

            if name.lower() == "done":
                break

            if name == "":
                print("Name cannot be empty.")
                continue

            #Keep asking until score is a valid integer
            while True:
                score_text = input(f"Score for {name}: ").strip()
                try:
                    score = int(score_text)
                    break
                except ValueError:
                    print("Invalid score. Enter a whole number.")

            #Save one record per line: name, score
            file.write(f"{name}, {score}\n")
            count += 1

    print(f"Saved {count} record(s) to golf.txt.")


def read_golf_scores():
    """
    Reads records from golf.txt file and displays them
    """
    try:
        with open("golf.txt", "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("\ngolf.txt does not exist yet. Add scores first.")
        return
    
    if not lines:
        print("\ngolf.txt is empty.")
        return
    
    print("\n=== Saved Golf Scores ===")
    for i, line in enumerate(lines, start=1):
        parts = line.split(",", 1)
        if len(parts) !=2:
            print(f"{i}. [Invalid record] {line}")
            continue

        name, score = parts
        print(f"{i}. {name}: {score}")

def main():
    """
    Main function to run the golf scores program
    """
    while True:
        print("\n=== Golf Score Management System ===")
        print("1. Enter golf scores")
        print("2. Display golf scores")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            write_golf_scores()
        elif choice == '2':
            read_golf_scores()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
