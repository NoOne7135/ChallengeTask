import pytest
from fastapi.testclient import TestClient
from main import app
from db import get_db, Bet


client = TestClient(app)

@pytest.fixture 
def setup_db():
    db = get_db()
    db.query(Bet).delete()
    db.commit()
    initial_balance = Bet(value=15000, type="init")#Adding a large amount for tests
    db.add(initial_balance)
    db.commit()
    return db

def test_1000_rolls(setup_db):
    bet = 10
    total_bets = 0
    total_wins = 0
    
    pair_count = 0
    full_house_count = 0
    large_straight_count = 0
    yahtzee_count = 0
    
    #You can replace 1000 with a lower or higher value, but with higher values ​​the database may return an error.
    for _ in range(1000):
        response = client.post("/api/roll", json={"bet": bet})
        assert response.status_code == 200
        winnings = response.json()["winnings"]

        if response.json()["winnings_type"] == "Yahtzee":
            yahtzee_count += 1
        
        elif response.json()["winnings_type"] == "Full House":
            full_house_count += 1
        
        elif response.json()["winnings_type"] == "Large Straight":
            large_straight_count += 1
        
        elif response.json()["winnings_type"] == "Pair":
            pair_count += 1
        
        total_bets += bet
        total_wins += winnings
    
    print(f"Pair = {pair_count}, Full House = {full_house_count}, Yahtzee = {yahtzee_count}, Large Straight = {large_straight_count}")

    rtp = (total_wins / total_bets) * 100
    print(f"Total Bets: {total_bets}, Total Wins: {total_wins}, RTP: {rtp}%")
    
    # Optional: Check if RTP is within a reasonable range (e.g., 90% - 100%)
    assert 90 <= rtp <= 100
