# ChallengeTask

## Create a Virtual Environment (Optional)

## Run Backend App

```bash
pip install -r requirements.txt
```
```bash
cd backend
```
```bash
uvicorn main:app --reload
```

## Run Frontend

```bash
cd frontend
```
```bash
npm i
```
```bash
npm run dev
```

## Run Odds Calculation

```bash
cd backend
```
```bash
python odds_calculation.py
```

## Run API Test

```bash
cd backend
```
```bash
pytest api_test.py -s
```

## Odds Calculation Result:
With the condition that Pair is only Pair, 2 Pairs are not taken into account  
Other: 0.0  
Pair: 1.43  
Full House: 2.86  
Yahtzee: 4.28  
Large Straight: 5.71  
