text
# Sports Betting Tracker & Dashboard API Documentation

---

## 🎲 Betting History API

### 1. Get Betting History

**Endpoint:**  
`GET /api/betting-history?userID={userID}`

**Description:**  
Retrieves raw betting history data for a specific user.

**Example Response:**
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

text

---

## 📚 Book Syncing API

### 1. Get Book Sync Data

**Endpoint:**  
`GET /api/book-sync`

**Description:**  
Fetches real-time sportsbook data from multiple betting platforms.

**Example Response:**
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

text

---

## 🔐 Authentication API

**Base URL:** `/auth`

### 1. Register a New User

**Endpoint:**  
`POST /auth/register`

**Description:**  
Registers a new user by email and password.

**Request Body:**
{
"email": "user@example.com",
"password": "securePassword123"
}

text
**Success Response:**
{
"msg": "User registered successfully",
"user_id": 1
}

text
**Error Response (400):**
{
"detail": "Email already registered"
}

text

### 2. Logging in a User

**Endpoint:**  
`POST /auth/login`

**Description:**  
Logs in user.

**Success Response (200 OK):**
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"token_type": "bearer"
}

text
**Error Response (401 Unauthorized):**
{
"detail" : "Invalid email or password"
}

text

---

## ⚙️ Settings API

**Base URL:**  
`/api/settings`

### 1. Get User Settings

**Endpoint:**  
`GET /api/settings?userID={userID}`

**Description:**  
Retrieves saved settings for the specified user.

**Example Response:**
{
"user_id": "abc123",
"theme": "dark",
"notifications": true,
"dashboard_layout": "compact"
}

text

### 2. Update User Settings

**Endpoint:**  
`PUT /api/settings`

**Description:**  
Updates the user's settings.

**Request Body:**
{
"user_id": "abc123",
"theme": "light",
"notifications": false,
"dashboard_layout": "expanded"
}

text
**Success Response:**
{ "msg": "Settings updated successfully" }

text
**Error Response (400):**
{ "detail": "Invalid settings data" }

text

---

## 👤 Profile API

**Base URL:**  
`/api/profile`

### 1. Get User Profile

**Endpoint:**  
`GET /api/profile?userID={userID}`

**Description:**  
Returns profile information for the specified user.

**Example Response:**
{
"user_id": "abc123",
"email": "user@example.com",
"display_name": "User123",
"join_date": "2024-05-15T12:00:00Z",
"avatar_url": "https://domain.com/img/avatar.png"
}

text

### 2. Update User Profile

**Endpoint:**  
`PUT /api/profile`

**Description:**  
Updates information in the user's profile.

**Request Body:**
{
"user_id": "abc123",
"display_name": "User456",
"avatar_url": "https://domain.com/img/avatar456.png"
}

text
**Success Response:**
{ "msg": "Profile updated successfully" }

text
**Error Response (400):**
{ "detail": "Invalid profile update data" }

text

---

## 📊 Dashboard API

**Base URL:**  
`/api/dashboard`

### 1. Get Dashboard Summary

**Endpoint:**  
`GET /api/dashboard?userID={userID}`

**Description:**  
Returns summary statistics and overview data for the user's dashboard.

**Example Response:**
{
"user_id": "abc123",
"total_bets": 120,
"total_wagered": 1500,
"total_won": 250,
"win_rate": 53.2,
"roi": 8.6,
"recent_bets": [
{ "bet_id": 123, "result": "W", "wager": 50, "payout": 95 },
{ "bet_id": 124, "result": "L", "wager": 30, "payout": 0 }
]
}

text

### 2. Get Dashboard Graph Data

**Endpoint:**  
`GET /api/dashboard/graphs?userID={userID}`

**Description:**  
Returns data formatted for dashboard charts (e.g., cumulative net profit, bet frequency over time).

**Example Response:**
{
"profit_over_time": [
{ "date": "2025-10-01", "profit": 25 },
{ "date": "2025-10-02", "profit": 35 }
],
"bets_by_sport": {
"NFL": 60,
"NBA": 40,
"NHL": 20
}
}

text

---

_Last updated: October 12, 2025_