import random
import time


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


moves = ['rock', 'paper', 'scissors', 'lizard', 'spock']


beats_map = {
    'rock': ['scissors', 'lizard'],
    'paper': ['rock', 'spock'],
    'scissors': ['paper', 'lizard'],
    'lizard': ['spock', 'paper'],
    'spock': ['scissors', 'rock'],
}


class Player:

    def move(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def learn(self, my_move, their_move):
        pass


class AllRockPlayer(Player):

    def move(self):
        return 'rock'


class RandomPlayer(Player):

    def move(self):
        return random.choice(moves)


class ReflectPlayer(Player):

    def __init__(self):
        self.their_last_move = None

    def move(self):
        if self.their_last_move is None:
            return random.choice(moves)
        else:
            return self.their_last_move

    def learn(self, my_move, their_move):
        self.their_last_move = their_move


class CyclePlayer(Player):

    def __init__(self):
        self.my_last_move = None

    def move(self):
        if self.my_last_move is None:
            move = random.choice(moves)
        else:
            idx = moves.index(self.my_last_move)
            move = moves[(idx + 1) % len(moves)]
        self.my_last_move = move
        return move

    def learn(self, my_move, their_move):
        self.my_last_move = my_move


class HumanPlayer(Player):

    def move(self):
        print(f"\n{Colors.BOLD}Your turn! Choose your move:{Colors.ENDC}")
        for i, move in enumerate(moves, start=1):
            print(f"  {Colors.OKCYAN}{i}{Colors.ENDC}: {move}")

        while True:
            choice = input("Enter the number or name of your move: ").lower().strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(moves):
                    selected_move = moves[index]
                    break
            elif choice in moves:
                selected_move = choice
                break

            print(
                f"{Colors.WARNING}Invalid input! Please enter a number between 1 and "
                f"{len(moves)} or a valid move name.{Colors.ENDC}"
            )

        print(f"Your choice: {Colors.OKGREEN}{selected_move}{Colors.ENDC}\n")
        return selected_move


def beats(one, two):
    return two in beats_map.get(one, [])


class Game:

    def __init__(self, p1, p2, rounds=3):
        self.p1 = p1
        self.p2 = p2
        self.rounds = rounds
        self.score_p1 = 0
        self.score_p2 = 0

    def play_round(self, round_number):
        print(f"{Colors.BOLD}Round {round_number} / {self.rounds}{Colors.ENDC}")
        print(f"Current Score => Player 1: {self.score_p1}  Player 2: {self.score_p2}\n")

        move1 = self.p1.move()
        move2 = self.p2.move()

        print(
            f"Player 1: {Colors.OKBLUE}{move1}{Colors.ENDC}  "
            f"Player 2: {Colors.OKGREEN}{move2}{Colors.ENDC}"
        )

        if beats(move1, move2):
            print(f"{Colors.OKBLUE}Player 1 wins this round{Colors.ENDC}")
            self.score_p1 += 1
        elif beats(move2, move1):
            print(f"{Colors.OKGREEN}Player 2 wins this round{Colors.ENDC}")
            self.score_p2 += 1
        else:
            print(f"{Colors.WARNING}It's a tie{Colors.ENDC}")

        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

        print(f"Score => Player 1: {self.score_p1}  Player 2: {self.score_p2}\n")
        time.sleep(1)

    def play_game(self):
        print(f"{Colors.HEADER}Game start{Colors.ENDC}")
        for round_number in range(1, self.rounds + 1):
            self.play_round(round_number)
        print(f"{Colors.HEADER}Game over!{Colors.ENDC}")

        if self.score_p1 > self.score_p2:
            print(
                f"{Colors.OKBLUE}Player 1 wins the game! Final score: "
                f"{self.score_p1} to {self.score_p2}{Colors.ENDC}"
            )
        elif self.score_p2 > self.score_p1:
            print(
                f"{Colors.OKGREEN}Player 2 wins the game! Final score: "
                f"{self.score_p2} to {self.score_p1}{Colors.ENDC}"
            )
        else:
            print(
                f"{Colors.WARNING}The game is a tie! Final score: "
                f"{self.score_p1} to {self.score_p2}{Colors.ENDC}"
            )


if __name__ == '__main__':
    print(f"{Colors.HEADER}Welcome to Rock, Paper, Scissors, Lizard, Spock!{Colors.ENDC}")

    opponents = {
        '1': AllRockPlayer,
        '2': RandomPlayer,
        '3': ReflectPlayer,
        '4': CyclePlayer,
    }

    print("\nChoose your opponent:")
    print(f"  {Colors.OKCYAN}1{Colors.ENDC}: AllRockPlayer (always plays 'rock')")
    print(f"  {Colors.OKCYAN}2{Colors.ENDC}: RandomPlayer (random moves)")
    print(f"  {Colors.OKCYAN}3{Colors.ENDC}: ReflectPlayer (imitates your last move)")
    print(f"  {Colors.OKCYAN}4{Colors.ENDC}: CyclePlayer (cycles through moves)")

    while True:
        choice = input("Enter the number of your opponent: ").strip()
        if choice in opponents:
            opponent = opponents[choice]()
            break

        print(f"{Colors.WARNING}Invalid choice. Try again.{Colors.ENDC}")

    while True:
        try:
            rounds = int(input("How many rounds would you like to play? "))
            if rounds > 0:
                break
            print(f"{Colors.WARNING}Please enter a positive number.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.WARNING}That's not a valid number.{Colors.ENDC}")

    game = Game(HumanPlayer(), opponent, rounds=rounds)
    game.play_game()
