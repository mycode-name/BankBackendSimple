from fastapi import FastAPI, Body, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json

app = FastAPI()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/ping")
def home():
    return "Pong!"


# Login App Part

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    with open("userdb.json", "r") as file:
        json_data = json.load(file)
        
    if json_data:
        password = json_data.get(form_data.username)
        if not password:
            raise HTTPException(status_code=403, detail="Incorrect username or password")
        
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/spend/history")
def spend_history(token: str = Depends(oauth_scheme)):
    #spend history logic here
    print("SPEND HISTORY", token)
    # spend history logic
    with open("spendHis.json", "r") as file:
        spend_history_data = json.load(file)
        if not spend_history_data.get(token):
            raise HTTPException(status_code=404, detail="No spend history found for this user")
    return {
        "username": token,
        "spend_history": spend_history_data[token]
    }
    
@app.get("/credit/history")
def credit_history(token: str = Depends(oauth_scheme)):
    #credit history logic here
    print("credit HISTORY", token)
    with open("creditHis.json", "r") as file:
        credit_history_data = json.load(file)
        if not credit_history_data.get(token):
            raise HTTPException(status_code=404, detail="No credit history found for this user")
    return {
        "username": token,
        "credit_history": credit_history_data[token]
    }
    
@app.post("/transfer/money")
def transfer_money(token: str = Depends(oauth_scheme), destination_usr: str = Body(...), amount_to_transfer: float = Body(...)):
    print(token)
    print(destination_usr)
    print(amount_to_transfer)
    
    with open("userBalance.json", "r") as file:
        user_balance_data = json.load(file)
        curr_user_bal = user_balance_data.get(token)["curr_balance"]
        print(f"Current User Balance: {curr_user_bal}")
        destination_usr_balDetails = user_balance_data.get(destination_usr)
        if not destination_usr_balDetails:
            raise HTTPException(status_code=404, detail="Destination user not found")
        destination_usr_bal = destination_usr_balDetails["curr_balance"]
        print(f"Destination User Balance: {destination_usr_bal}")
        if curr_user_bal < amount_to_transfer:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        # Update balances
    user_balance_data[token]["curr_balance"] -= amount_to_transfer
    user_balance_data[destination_usr]["curr_balance"] += amount_to_transfer
    with open("userBalance.json", "w") as file:
        json.dump(user_balance_data, file, indent=4)
    return {
        "username": token,
        "destination_user": destination_usr,
        "amount_transferred": amount_to_transfer,
        "new_balance": user_balance_data[token]["curr_balance"]
    }
    
@app.get("/userbalance")
def get_userbalance(token: str = Depends(oauth_scheme)):
    with open("userBalance.json", "r") as file:
        user_data = json.load(file)
        if not user_data.get(token):
            raise HTTPException(status_code=404, detail="No balance details found for this user")
    return {
        "username": token,
        "balance": user_data[token]["curr_balance"]
    }