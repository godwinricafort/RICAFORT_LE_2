import os
import random
from .user_manager import UserManager
from .score import Score

class DiceGame(UserManager):
	
	def __init__(self):
		super().__init__()
		self.scores = {}
		self.ranking_text_filepath = ""
		self.load_scores()
		self.game_id = 0

	def load_scores(self):
		current_dir = os.path.dirname(os.path.abspath(__file__))
		root_dir = os.path.dirname(current_dir)
		folder_name = "data"
		new_folder_path = os.path.join(root_dir, folder_name)
		os.makedirs(new_folder_path, exist_ok=True)

		ranking_txt_filename = "ranking.txt"
		self.ranking_text_filepath = os.path.join(new_folder_path, ranking_txt_filename)

		file = open(self.ranking_text_filepath, 'w')
		file.close() 

	def save_user_scores(self, points, wins):
		self.game_id += 1
		self.scores[self.game_id] = Score(self.current_user, self.game_id, points, wins)

		sorted_scores = sorted(self.scores.values(), key=lambda x: (-x.points, -x.wins))

		with open(self.ranking_text_filepath, 'w') as file: 
			rank = 1
			for score in sorted_scores:
				file.write(f"{rank}. {score.username}: Points {score.points}, Wins - {score.wins}\n")
				rank += 1


	def start_game(self):
		user_points = 0
		wins = 0

		TOTAL_ROUNDS = 3
		current_round = 0
		current_points = 0

		user_roll = 0
		cpu_roll = 0

		def roll_dice():
			return random.randint(1, 6)

		print(f"Starting game as {self.current_user}.")
		
		while True:
			while current_round != TOTAL_ROUNDS:
				user_roll = roll_dice()
				cpu_roll = roll_dice()

				print(f"{self.current_user} rolled: {user_roll}")
				print(f"CPU rolled: {cpu_roll}\n")

				if user_roll == cpu_roll:
					print("It's a draw!\n")
					continue

				if user_roll > cpu_roll:
					print(f"You win this round, {self.current_user}!\n")
					current_points += 1
					current_round += 1
					continue

				if user_roll < cpu_roll:
					print(f"You lost this round, {self.current_user}.\n")
					current_round += 1
					continue

			user_points += current_points
			if current_points >= 2:
				user_points += TOTAL_ROUNDS
				wins += 1
				print(f"{self.current_user}")
				print(f"Total Points: {user_points}, Stages Won: {wins}")
				choice = int(input("Do you want to continue to the next stage? (1 for Yes, 0 for No): "))
				match choice: 
					case 0: 
						print(f"GAME OVER. You won {wins} stages, with a total of {user_points}points!\n")
						self.save_user_scores(user_points, wins)
						break
					case 1: 
						current_round = 1
						current_points = 0
						continue
			else: 
				print(f"You lost this stage, {self.current_user}.\n")
				if wins: 
					print(f"GAME OVER. You won {wins} stages, with a total of {user_points} points!\n")
				else: 
					print("GAME OVER. You didn't win any stages.\n")
				self.save_user_scores(user_points, wins)
				break

			return


	def top_ranking_scores(self):
		if not self.scores:
			print("You haven't played a game yet. Play a game to see the top ranking scores.")
			return

		sorted_scores = sorted(self.scores.values(), key=lambda x: (-x.points, -x.wins))

		print("Top Scores:")
		rank = 1
		for score in sorted_scores:
			print(f"{rank}. {score.username}: Points {score.points}, Wins - {score.wins}")
			rank += 1

	def logout(self):
		self.current_user = None
		print("Logged out")
		return

	def menu(self):
		while True:
			if self.current_user:
				print(f"\nWelcome, {self.current_user}!")
				options = ["Start Game", "Show top scores", "Logout"]
				print("Welcome to Dice Roll Game!")
				for o in range(len(options)):
					print(f"{o+1}. {options[o]}")

				try:
					choice = int(input("\nEnter your choice, or leave blank to cancel: "))
				except: 
					print("Invalid choice! Please try again.")
					continue

				match choice:
					case 1:
						self.start_game()
					case 2: 
						self.top_ranking_scores()
					case 3:
						self.logout()
						continue
			else:
				options = ["Register", "Login", "Exit"]
				print("\nWelcome to Dice Roll Game!")
				for o in range(len(options)):
					print(f"{o+1}. {options[o]}")

				try:
					choice= int(input("\nEnter your choice, or leave blank to cancel: "))
				except: 
					print("Invalid choice! Please try again.")
					continue

				match choice:
					case 1:
						self.user_register()
					case 2: 
						self.login()
					case 3:
						print("Exiting...")
						break

		return