Create a virtual environment (optional)


Run backend:

pip install -r requirements.txt

cd backend

uvicorn main:app --reload


Run frontend:

cd frontend

npm i 

npm run dev


Run odds_calculation:

cd backend

python odds_calculation.py 


Run api_test: (Without changing the odds, the test will fail with an RTP value of 0.6 – 0.7; when changing the odds, the test will be passed with an RTP value of 0.93 - 0.97, requires 90 seconds)

cd backend

pytest api_test.py -s


odds_calculation result:

With the condition that Pair is only Pair, 2 Pairs are not taken into account.
Other: 0.0
Pair: 1.43
Full house: 2.86
Yahtzee: 4.28
Large Straight: 5.71
