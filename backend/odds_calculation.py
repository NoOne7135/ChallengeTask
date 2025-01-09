import random
from collections import Counter


class DiceGame:
    def __init__(self):
        self.coefficients = {
            "Yahtzee": 3.0,
            "Large Straight": 4.0,
            "Full house": 2.0,
            "Pair": 1.0,
            "Other": 0.0,
        }
        
    def roll_dice(self):
        return [random.randint(1, 6) for _ in range(5)]

    def evaluate_combination(self, dice):
            counts = Counter(dice)
    
            if 5 in counts.values():
                return "Yahtzee"
            elif sorted(dice) == list(range(min(dice), min(dice) + 5)):
                return "Large Straight"
            elif sorted(counts.values()) == [2, 3]:
                return "Full house"
            elif list(counts.values()).count(2) == 1:
                return "Pair"
            else:
                return "Other"

    def run_simulation(self, rounds):
        total_bets = 0
        total_payouts = 0
        combination_counts = {key: 0 for key in self.coefficients} 

        for _ in range(rounds):
            bet = 10
            total_bets += bet
            roll = self.roll_dice()
            outcome = self.evaluate_combination(roll)
            total_payouts += bet * self.coefficients[outcome]
            combination_counts[outcome] += 1 

        rtp = total_payouts / total_bets
        return rtp, combination_counts

    def adjust_coefficients(self, target_rtp=0.95, iterations=1000000):
        simulated_rtp, _ = self.run_simulation(iterations)
        adjustment_factor = target_rtp / simulated_rtp

        for key in self.coefficients:
            if key != "Other":
                self.coefficients[key] = round(self.coefficients[key] * adjustment_factor, 2)

        return self.coefficients

if __name__ == "__main__":
    game = DiceGame()

    print("Initial Coefficients:", game.coefficients)
    initial_rtp, initial_counts = game.run_simulation(1000000)
    print(f"Initial RTP: {initial_rtp * 100:.2f}%")
    print("Combination Counts (Initial):", initial_counts)

    print("\nAdjusting coefficients for target RTP of 95%...")
    optimized_coeffs = game.adjust_coefficients(target_rtp=0.95)
    print("Optimized Coefficients:", optimized_coeffs)

    adjusted_rtp, adjusted_counts = game.run_simulation(1000000)
    print(f"Adjusted RTP: {adjusted_rtp * 100:.2f}%")
    print("Combination Counts (Adjusted):", adjusted_counts)
