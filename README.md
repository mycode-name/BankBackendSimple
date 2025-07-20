# 💰 Simple Bank Backend API

This is a basic **banking backend API** built using **FastAPI**. It provides endpoints for user authentication, viewing transaction history (credit/spend), checking account balance, and transferring money between users. Data is persisted using local JSON files.

## 🚀 Features

- 🔐 Token-based authentication (OAuth2)
- 📜 Login endpoint using `OAuth2PasswordRequestForm`
- 💸 Transfer money between users
- 📈 View credit and spending history
- 💼 Get current user balance

## 📁 Project Structure

```bash
.
├── main.py                # Main FastAPI app with endpoints
├── userdb.json            # Stores usernames and their passwords (plain text - for demo only)
├── userBalance.json       # Stores current balance per user
├── spendHis.json          # Stores spending history per user
├── creditHis.json         # Stores credit history per user
````

---

## 🔐 Authentication

Authentication is done using `OAuth2PasswordBearer` with username as the token. This is **not production secure** (no JWT, no hashing).

### 🔑 Sample login request

```
POST /token
Content-Type: application/x-www-form-urlencoded

username=john&password=1234
```

Response:

```json
{
  "access_token": "john",
  "token_type": "bearer"
}
```

Use this `access_token` as the Bearer token in the `Authorization` header for other protected endpoints.

---

## 📡 API Endpoints

### `GET /ping`

Health check route.

* ✅ No auth required
* 🔁 Response: `"Pong!"`

---

### `POST /token`

Login and receive bearer token.

* 📥 Body: `username`, `password` (form data)

---

### `GET /spend/history`

Get spending history for the logged-in user.

* 🔐 Requires Bearer token

---

### `GET /credit/history`

Get credit history for the logged-in user.

* 🔐 Requires Bearer token

---

### `GET /userbalance`

Check current balance of the logged-in user.

* 🔐 Requires Bearer token

---

### `POST /transfer/money`

Transfer money from logged-in user to another user.

#### 🔽 Body (JSON):

```json
{
  "destination_usr": "alice",
  "amount_to_transfer": 200
}
```

* 🔐 Requires Bearer token
* ❗ Fails if insufficient balance or user not found

---

## ⚠️ Disclaimer

This project is for **educational/demo purposes only**:

---

## 🛠 Tech Stack

* **Python 3.9+**
* **FastAPI**
* **JSON (for data storage)**

---

## 📌 Run Locally

1. Install dependencies:

```bash
pip install fastapi uvicorn python-multipart
```

2. Start the server:

```bash
uvicorn main:app --reload
```

3. Test the API at:

```
http://127.0.0.1:8000/docs
```

Interactive Swagger UI will be available at `/docs`.

---

## 🧪 Example Test Users

Add test users to `userdb.json`, like:

```json
{
  "john": "1234",
  "alice": "pass"
}
```

And initialize their balances in `userBalance.json`:

```json
{
  "john": {
    "curr_balance": 1000
  },
  "alice": {
    "curr_balance": 1500
  }
}
```

---
