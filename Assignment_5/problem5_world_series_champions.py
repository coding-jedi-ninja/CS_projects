# I confirm that AI code completion tools were disabled while writing this program.
# Name: Arja Sadhukhan
# NU ID: 003163346

"""
Problem 5: World Series Champions

You are given a file named WorldSeriesWinners.txt. This file contains a chronological list of 
the World Series winning teams from 1903 through 2009. (The first line in the file is the name 
of the team that won in 1903, and the last line is the name of the team that won in 2009. Note 
the World Series was not played in 1904 or 1994.) 

Write a program that lets the user enter the name of a team, then displays the number of times 
that team has won the World Series in the time period from 1903 through 2009.
"""


def count_world_series_wins(team_name):
    """
    Counts how many times a team won the World Series from 1903-2009
    
    Args:
        team_name (str): The name of the team to search for
        
    Returns:
        int: The number of times the team won the World Series
    """
    filename = "WorldSeriesWinners.txt"

    #Open the file and read all lines into a list
    with open(filename, "r") as file:
        winners = file.readlines()

    #Clean each line (remove extra spaces/newline)
    winners = [team.strip() for team in winners]

    #Count how many times the given team appears
    win_count = winners.count(team_name)

    return win_count


def main():
    """
    Main function to run the World Series Champions program
    """
    print("World Series Champions (1903-2009)")
    print("Enter a team name exactly as it appears in the file.\n")

    team_name = input("Team name: ").strip()

    try:
        wins = count_world_series_wins(team_name)
        print(f"\n{team_name} won the World Series {wins} time(s) from 1903 to 2009.")
    except FileNotFoundError:
        print("Error: WorldSeriesWinners.txt was not found in this folder.")


if __name__ == "__main__":
    main()
