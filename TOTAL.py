from datetime import datetime
import json

# team.py
class Team:
    """
    Represents a hockey team.
    """
    fee_amount = 100  # Example participation fee

    def __init__(self, team_id, name, gender, fee_paid=False, cancellation_date=None):
        self.__id = team_id  # Unique identifier
        self.__date = datetime.now().strftime("%Y-%m-%d")  # Auto-generated timestamp
        self.name = name  # Team name
        self.gender = gender  # Gender: 'boys' or 'girls'
        self.fee_paid = fee_paid  # Boolean flag for payment status
        self.cancellation_date = cancellation_date  # Date when the team cancels participation

    @property
    def id(self):
        return self.__id

    @property
    def date(self):
        return self.__date

    def cancel_participation(self):
        self.cancellation_date = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "id": self.__id,
            "date": self.__date,
            "name": self.name,
            "gender": self.gender,
            "fee_paid": self.fee_paid,
            "cancellation_date": self.cancellation_date,
        }

    def __str__(self):
        return f"ID: {self.__id}, Date: {self.__date}, Name: {self.name}, Gender: {self.gender}, Fee Paid: {self.fee_paid}, Cancellation Date: {self.cancellation_date}" 


# team_manager.py
class TeamManager:
    """
    Manages CRUD operations for teams.
    """
    def __init__(self):
        self.teams = {}  # Dictionary to store teams by their ID
        self.next_id = 1  # Auto-incrementing ID

    def create_team(self, name, gender, fee_paid=False):
        team = Team(self.next_id, name, gender, fee_paid)
        self.teams[self.next_id] = team
        self.next_id += 1
        print("Team created successfully.")

    def read_team(self, team_id):
        return self.teams.get(team_id, "Team not found.")

    def update_team(self, team_id, name=None, gender=None, fee_paid=None):
        if team_id not in self.teams:
            print("Team not found.")
            return
        if name:
            self.teams[team_id].name = name
        if gender:
            self.teams[team_id].gender = gender
        if fee_paid is not None:
            self.teams[team_id].fee_paid = fee_paid
        print("Team updated successfully.")

    def delete_team(self, team_id):
        if team_id in self.teams:
            del self.teams[team_id]
            print("Team deleted successfully.")
        else:
            print("Team not found.")

    def list_teams(self, gender=None):
        for team in self.teams.values():
            if gender is None or team.gender == gender:
                print(team)

    def cancel_team(self, team_id):
        if team_id in self.teams:
            self.teams[team_id].cancel_participation()
            print("Team participation cancelled.")
        else:
            print("Team not found.")

    def show_statistics(self):
        total_teams = len(self.teams)
        paid_teams = sum(1 for team in self.teams.values() if team.fee_paid)
        percent_paid = (paid_teams / total_teams * 100) if total_teams > 0 else 0
        print(f"Total Teams: {total_teams}, Fee Paid: {percent_paid:.2f}%")

    def save_to_file(self, filename="teams.txt"):
        with open(filename, "w") as file:
            json.dump([team.to_dict() for team in self.teams.values()], file)
        print("Teams saved to file.")

    def load_from_file(self, filename="teams.txt"):
        try:
            with open(filename, "r") as file:
                teams_data = json.load(file)
                self.teams.clear()
                for data in teams_data:
                    team = Team(data["id"], data["name"], data["gender"], data["fee_paid"], data["cancellation_date"])
                    self.teams[data["id"]] = team
            print("Teams loaded from file.")
        except FileNotFoundError:
            print("No saved team file found.")


# user_interface.py
class UserInterface:
    """
    Handles user interaction through a command-line menu.
    """
    def __init__(self, team_manager):
        self.team_manager = team_manager

    def display_menu(self):
        while True:
            print("\nYouth Hockey Cup - Team Management")
            print("1. Create a new team")
            print("2. View a team")
            print("3. Update a team")
            print("4. Delete a team")
            print("5. List all teams")
            print("6. List teams by gender")
            print("7. Show statistics")
            print("8. Cancel team participation")
            print("9. Save teams to file")
            print("10. Load teams from file")
            print("11. Quit")
            choice = input("Select an option: ")

            if choice == "1":
                name = input("Enter team name: ")
                gender = input("Enter gender (boys/girls): ")
                fee_paid = input("Has the fee been paid? (yes/no): ").strip().lower() == "yes"
                self.team_manager.create_team(name, gender, fee_paid)
            elif choice == "2":
                team_id = int(input("Enter team ID: "))
                print(self.team_manager.read_team(team_id))
            elif choice == "3":
                team_id = int(input("Enter team ID: "))
                name = input("Enter new name (leave blank to keep current): ") or None
                gender = input("Enter new gender (boys/girls, leave blank to keep current): ") or None
                fee_paid = input("Has the fee been paid? (yes/no, leave blank to keep current): ")
                fee_paid = None if fee_paid == "" else fee_paid.strip().lower() == "yes"
                self.team_manager.update_team(team_id, name, gender, fee_paid)
            elif choice == "4":
                team_id = int(input("Enter team ID: "))
                self.team_manager.delete_team(team_id)
            elif choice == "5":
                self.team_manager.list_teams()
            elif choice == "6":
                gender = input("Enter gender (boys/girls): ")
                self.team_manager.list_teams(gender)
            elif choice == "7":
                self.team_manager.show_statistics()
            elif choice == "8":
                team_id = int(input("Enter team ID to cancel participation: "))
                self.team_manager.cancel_team(team_id)
            elif choice == "9":
                self.team_manager.save_to_file()
            elif choice == "10":
                self.team_manager.load_from_file()
            elif choice == "11":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice, please try again.")

# main.py
if __name__ == "__main__":
    team_manager = TeamManager()
    ui = UserInterface(team_manager)
    ui.display_menu()
