## Betting History API

## API Documentation

### 1. Get Betting History
**Endpoint:** `GET /api/betting-history?userID={userID}`
**Description:** Retrieves raw betting history data for a specific user. 
**Notes:** JSON exapmple below. Feel free to edit however.
**TO ADD: backend/app/betting-history**

**Example Response**
```json
[
  {
    "bet_id": 123,
    "user_id": "abc123",
    "wager": 50,
    "bet_type": "Player Prop",
    "bet_subtype": "Saquon Barkley +110 Total Yards",
    "odds": "-100",
    "result": "W",
    "timestamp": "2025-10-10T14:30:00Z"
  }
]
```

## 📚 Book Syncing API

### 1. Get Book Sync Data
**Endpoint:** `GET /api/book-sync`  
**Description:** Fetches real-time sportsbook data from multiple betting platforms.  
**Returns:** A large JSON object containing odds, lines, and available bets across different books. **TO ADD: backend/app/booksync**

**Example Response**
```json
{
  "timestamp": "2025-10-10T15:45:00Z",
  "books": [
    {
      "name": "DraftKings",
      "sports": [
        {
          "sport": "NFL",
          "bets": [
            { "event": "Bears vs Packers", "type": "Moneyline", "odds": { "Bears": "+180", "Packers": "-220" } },
            { "event": "Eagles vs Cowboys", "type": "Spread", "odds": { "Eagles": "-3.5 (-110)", "Cowboys": "+3.5 (-110)" } }
          ]
        },
        {
          "sport": "NBA",
          "bets": [
            { "event": "Lakers vs Celtics", "type": "Over/Under", "odds": { "Over 228.5": "-115", "Under 228.5": "-105" } }
          ]
        }
      ]
    },
    {
      "name": "FanDuel",
      "sports": [
        {
          "sport": "NFL",
          "bets": [
            { "event": "Bears vs Packers", "type": "Moneyline", "odds": { "Bears": "+190", "Packers": "-230" } },
            { "event": "Eagles vs Cowboys", "type": "Spread", "odds": { "Eagles": "-3 (-110)", "Cowboys": "+3 (-110)" } }
          ]
        }
      ]
    }
  ]
}

```

## 🔐 Authentication API

### Base URL
`/auth`

### 1. Register a New User
**Endpoint:** `POST /auth/register`  
**Description:** Registers a new user by email and password. 

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
**Success**
```json
{
  "msg": "User registered successfully",
  "user_id": 1
}
```
**Error Response (400)**
```json
{
  "detail": "Email already registered"
}
```

### Logging in a User
**Endpoint:** `POST /auth/login`
**Description** Logs in user.

**Responses**

**200 OK**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
**401 Unauthorized**
```json
{
    "detail" : "Invalid email or password"
}
```

