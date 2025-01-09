from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import Bet, get_db
from sqlalchemy.orm import Session
import random


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RollRequest(BaseModel):
    bet: int

class RollResponse(BaseModel):
    dice: list[int]
    winnings: float
    winnings_type: str 
    balance: float 
    
@app.get("/api/multipliers", response_model=dict)
def get_multipliers():
    return {
        "Pair": 1,
        "Full House": 2,
        "Yahtzee": 3,
        "Large Straight": 4,
        "Other": 0
    }
    
@app.get("/api/balance", response_model=float)
def get_balance(db: Session = Depends(get_db)):
    balance_record = db.query(Bet).filter(Bet.type == "init").first()
    
    if balance_record is None:
        balance_record = Bet(value=1000, type="init")
        db.add(balance_record)
        db.commit()

    return round(balance_record.value, 2)

@app.post("/api/roll", response_model=RollResponse)
def roll_dice(request: RollRequest, db: Session = Depends(get_db)):
    balance_record = db.query(Bet).filter(Bet.type == "init").first()
    
    if not balance_record:
        return {"error": "Balance not found."}
    
    balance = balance_record.value

    if request.bet > balance:
        return {"error": "Not enough balance."}

    balance_record.value -= request.bet
    db.commit()

    dice = [random.randint(1, 6) for _ in range(5)]
    winnings = 0
    winnings_type = 'Ohter'
    counts = {x: dice.count(x) for x in set(dice)}
    
    if sorted(dice) == list(range(min(dice), min(dice) + 5)):
        winnings = request.bet * get_multipliers()["Large Straight"]  # Large Straight
        winnings_type = 'Large Straight'
        
    elif 5 in counts.values():
        winnings = request.bet * get_multipliers()["Yahtzee"]  # Yahtzee
        winnings_type = 'Yahtzee'
        
    elif sorted(counts.values()) == [2, 3]:
        winnings = request.bet * get_multipliers()["Full House"]  # Full House
        winnings_type = 'Full House'
        
    elif list(counts.values()).count(2) == 1: 
        winnings = request.bet * get_multipliers()["Pair"] # Pair
        winnings_type = 'Pair'

    if winnings > 0:
        balance_record.value += winnings
        db.add(Bet(value=winnings, type="Win"))
        
    else:
        db.add(Bet(value=-request.bet, type="Bet"))

    db.commit()

    return {"dice": dice, "winnings": winnings, "winnings_type": winnings_type, "balance": round(balance_record.value, 2)}