<template>
  <div class="game-container">
    <div class="dice-section">
      <h2>Dice</h2>
      <div class="dice">
        <div v-for="(die, index) in dice" :key="index" class="die animate-die">
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
import { ref, reactive, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const dice = ref([null, null, null, null, null]);
    const balance = ref(100);
    const bet = ref(0);
    const highlighted = ref("");
    const multipliers = reactive({});
    const isRolling = ref(false);

    const fetchInitialData = async () => {
      try {
        const balanceResponse = await axios.get("http://127.0.0.1:8000/api/balance");
        balance.value = balanceResponse.data;

        const multipliersResponse = await axios.get("http://127.0.0.1:8000/api/multipliers");
        Object.assign(multipliers, multipliersResponse.data);
      } catch (error) {
        console.error("Error loading initial data:", error);
      }
    };

    const rollDice = async () => {
      if (bet.value > balance.value || bet.value <= 0) {
        alert("Invalid bet!");
        return;
      }

      isRolling.value = true;

      try {
        balance.value -= bet.value;

        // Визуальная задержка для анимации броска
        dice.value = [null, null, null, null, null]; // Сбрасываем кубики для "анимации"
        await new Promise(resolve => setTimeout(resolve, 1000)); // 1 секунда ожидания

        const response = await axios.post("http://127.0.0.1:8000/api/roll", { bet: bet.value });
        dice.value = response.data.dice; // Обновляем кубики
        balance.value = response.data.balance;

        highlighted.value = response.data.winnings > 0
          ? response.data.winnings_type
          : "Other";
      } catch (error) {
        console.error("Error rolling dice:", error);
        alert("An error occurred while rolling the dice.");
        balance.value += bet.value;
      } finally {
        isRolling.value = false;
      }
    };

    onMounted(fetchInitialData);

    return {
      dice,
      balance,
      bet,
      highlighted,
      multipliers,
      isRolling,
      rollDice,
    };
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

/* Анимация кубиков */
.animate-die {
  animation: bounce 0.5s ease-in-out;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
