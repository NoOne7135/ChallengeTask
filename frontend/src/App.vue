<template>
  <div class="game-container">
    <div class="dice-section">
      <h2>Dice</h2>
      <div class="dice">
        <div v-for="(die, index) in dice" :key="index" class="die">
          {{ die === null ? '?' : die }}
        </div>
      </div>
    </div>

    <div class="prices-section">
      <h3>Prices</h3>
      <ul>
        <li :class="{'highlight': highlighted === 'Pair'}">Pair: x{{ multipliers.Pair || '?' }}</li>
        <li :class="{'highlight': highlighted === 'Full House'}">Full house: x{{ multipliers['Full House'] || '?' }}</li>
        <li :class="{'highlight': highlighted === 'Yahtzee'}">Yahtzee: x{{ multipliers.Yahtzee || '?' }}</li>
        <li :class="{'highlight': highlighted === 'Large Straight'}">Large Straight: x{{ multipliers['Large Straight'] || '?' }}</li>
        <li :class="{'highlight': highlighted === 'Other'}">Other: x{{ multipliers.Other || '0' }}</li>
      </ul>
    </div>

    <div class="bet-section">
      <h3>Bet</h3>
      <input type="number" v-model.number="bet" min="0" :max="balance" />
      <button :disabled="bet > balance || bet <= 0 || isRolling" @click="rollDice">ROLL</button>
    </div>

    <div class="balance-section">
      <h3>Your balance</h3>
      <p>{{ balance }}</p>
    </div>

    <!-- Loader animation -->
    <div v-if="isRolling" class="loader"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
  return {
      dice: [null, null, null, null, null],
      balance: 100, // Start with 100, will be replaced by backend value
      bet: 0, // Current bet
      highlighted: "", // Store the highlighted prize
      multipliers: {}, // Store the multipliers from backend
      isRolling: false, // Track if the dice rolling is in progress
    };
  },
  async created() {
    try {
      // Fetch the initial balance
      const balanceResponse = await axios.get("http://127.0.0.1:8000/api/balance");
      this.balance = balanceResponse.data;

      // Fetch the multipliers
      const multipliersResponse = await axios.get("http://127.0.0.1:8000/api/multipliers");
      this.multipliers = multipliersResponse.data;
    } catch (error) {
      console.error("Error loading initial data:", error);
    }
  },
  methods: {
    async rollDice() {
      if (this.bet > this.balance || this.bet <= 0) {
        alert("Invalid bet!");
        return;
      }

      this.isRolling = true; // Show the loader during the process

      try {
        // Deduct the bet from balance
        this.balance -= this.bet;

        // Add a small delay before making the request (e.g., 1 second)
        await new Promise(resolve => setTimeout(resolve, 1000)); // 1000ms = 1 second

        // Make request to API to get dice result
        const response = await axios.post("http://127.0.0.1:8000/api/roll", { bet: this.bet });
        
        // Update dice and balance
        this.dice = response.data.dice;
        this.balance = response.data.balance;

        // Handle winnings and highlight the correct prize
        if (response.data.winnings > 0) {
          if (response.data.winnings_type === "Yahtzee") {
            this.highlighted = "Yahtzee";
          } else if (response.data.winnings_type === "Full House") {
            this.highlighted = "Full House";
          } else if (response.data.winnings_type === "Large Straight") {
            this.highlighted = "Large Straight";
          } else if (response.data.winnings_type === "Pair") {
            this.highlighted = "Pair";
          } else {
            this.highlighted = "Other";
          }
        } else {
          this.highlighted = "Other";
        }
        
      } catch (error) {
        console.error("Error rolling dice:", error);
        alert("An error occurred while rolling the dice.");
        
        // Refund the bet if there's an error
        this.balance += this.bet;
      } finally {
        this.isRolling = false; // Hide the loader when done
      }
    },
  },
};
</script>

<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.dice-section, .prices-section, .bet-section, .balance-section {
  text-align: center;
}

.dice {
  display: flex;
  gap: 10px;
}

.die {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #000;
  font-size: 24px;
  font-weight: bold;
}

ul {
  list-style-type: none;
  padding: 0;
}

li.highlight {
  background-color: yellow;
  font-weight: bold;
  color: black;
}

/* Loader styles */
.loader {
  border: 8px solid #f3f3f3;
  border-top: 8px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-top: 20px;
}

/* Spinner animation */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>