# System Design Flashcards

A flashcard web app to help study system design concepts, built as part of Assignment 1 for the Web Development course. The app lets you flip through cards one at a time, bookmark the ones you want to revisit, and manage your own card library. This app is further extended under part 2 and now supports user accounts, review history tracking, and an admin panel.

---

## What problem does this solve?

I wanted to build something I'd actually use. System design is one of those topics where there's a lot to remember, and I always struggled with keeping track of what I'd reviewed and what I hadn't before an important interview. I seeded it with 101 real system design questions I found useful, but you can also add more as and when I learn or explore new concepts, edit, or delete on your own. I can also bookmark some of the questions for revisions just before the interviews using favourite flag to update and add new questions.

---

## Tech Stack

| Layer | What I used |
|---|---|
| Frontend | React 18 + Vite |
| Styling | Plain CSS (no external library) |
| Backend | FastAPI (Python) |
| Database | MongoDB Atlas (free cloud tier) |
| DB connection | Motor (async Python driver) |
| HTTP requests | Axios |
| Auth | JWT (python-jose) + bcrypt (passlib) |

Here's roughly how it all connects:

```
Browser (React on port 5173)
        ↕  Axios (HTTP requests + Bearer token)
FastAPI server (Python on port 8000)
        ↕  Motor async driver
MongoDB Atlas (cloud database)
```

---

## Features

- Single page app, no entire page reloads, React handles everything dynamically on a single page just by updating the content
- One card shown at a time, click to flip, then hit Next to move on
- 101 pre-loaded system design cards across Easy, Medium, and Hard which is feeded to the DB using seed.py to generate the JSON data
- Filter cards by difficulty i.e, All, Easy, Medium, Hard
- Bookmark cards with the bookmark icon to save them for later
- Filter by favourites to only see bookmarked cards for a quick review
- Live search, type to filter cards by question or answer text, stacks on top of the active difficulty and favourites filter
- Add your own flashcards with question, answer, category and difficulty
- Edit any card — changes take effect immediately and reset the deck
- Delete cards you don't need anymore
- Progress bar tracks how many cards you've reviewed vs how many are left
- Reset button to start the deck over
- Works on mobile view too
- If the backend goes down, the app shows an error message instead of a blank screen

### Part 2 (feature extensions and enhancements)
- Register and log in with email and password — JWT token issued on login
- Token stored in localStorage and automatically attached to every request
- Click your name in the header to open your profile — update username/email or delete your account
- Every card you click Next on gets recorded as a review event with a timestamp
- Admin panel (admin users only),view all registered users, see their full review history, promote/demote admin status, delete users
- Live search on the admin dashboard, filter users by name or email instantly
- All flashcard routes are protected, unauthenticated requests get a 401
- First admin has to be created directly via the API docs or MongoDB Atlas, after that admins can promote others through the panel

---

## Folder Structure

```
flashcard-app/
├── README.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app + CORS setup
│   │   ├── database.py              # MongoDB connection (with certifi SSL fix)
│   │   ├── auth.py                  # JWT creation, password hashing, Depends guards
│   │   ├── models/
│   │   │   ├── flashcard.py         # Data shape for create / update / response
│   │   │   └── user.py              # UserRegister, UserLogin, UserResponse, TokenResponse
│   │   └── routes/
│   │       ├── flashcardAPIs.py     # Flashcard CRUD + review history create
│   │       ├── authRoutes.py        # Register, login, /me (read, update, delete)
│   │       └── adminRoutes.py       # Admin-only user management + history read/delete
│   ├── seed.py                      # Run once to load 101 cards into the DB
│   ├── requirements.txt
│   └── .env                         # MongoDB URL + SECRET_KEY — not committed to GitHub, added the pattern under gitignore
└── frontend/
    └── src/
        ├── components/
        │   ├── BookmarkIcon.jsx      # SVG bookmark icon (outline or filled)
        │   ├── FlashcardDeck.jsx     # Main component that manages everything
        │   ├── FlashcardCard.jsx     # The actual card with flip animation
        │   ├── FilterBar.jsx         # Difficulty, favourites filters + live search input
        │   ├── ProgressBar.jsx       # Shows reviewed vs remaining
        │   ├── AddCardModal.jsx      # Form to create a new card
        │   ├── EditCardModal.jsx     # Form to edit an existing card
        │   ├── LoginModal.jsx        # Login form
        │   ├── RegisterModal.jsx     # Register form
        │   ├── ProfileModal.jsx      # View / edit / delete own account
        │   └── AdminPanel.jsx        # Admin panel — users + history + live search
        ├── context/
        │   └── AuthContext.jsx       # Global auth state, login/register/logout functions
        ├── hooks/
        │   └── useFlashcards.js      # Custom hook — flashcard data, state, search filtering
        ├── services/
        │   └── api.js                # All axios calls + Bearer token interceptor
        ├── App.jsx
        └── index.css                 # Central place for all the styling used in the App
```

---

## How to run it

### You'll need
- Python 3.10+
- Node.js 18+
- A free MongoDB Atlas account

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add a `.env` file inside `backend/`:
```
MONGODB_URL=your_atlas_connection_string
DB_NAME=flashcard_db
SECRET_KEY=your_random_secret_key
```

Load the flashcards into the database:
```bash
python3 seed.py
```

Start the server:
```bash
uvicorn app.main:app --reload
```

You can test and read the documentation for all the API endpoints at `http://localhost:8000/docs`, FastAPI generates this automatically which was really handy.

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` and it should work.

---

## CRUD operations

Three entities — Flashcard, User, and History — each with full or appropriate CRUD coverage.

### Flashcard
| Operation | Endpoint | What it does |
|---|---|---|
| Create | POST `/api/flashcards/` | Add a new card |
| Read | GET `/api/flashcards/` | Get all cards (filter by difficulty or favourite) |
| Read | GET `/api/flashcards/{id}` | Get one card |
| Update | PUT `/api/flashcards/{id}` | Edit a card or toggle bookmark |
| Delete | DELETE `/api/flashcards/{id}` | Delete a card (returns 204) |

### User
| Operation | Endpoint | What it does |
|---|---|---|
| Create | POST `/api/auth/register` | Register a new account |
| Read | GET `/api/auth/me` | Get your own profile |
| Update | PUT `/api/auth/me` | Update username or email |
| Delete | DELETE `/api/auth/me` | Delete your own account |

### History
| Operation | Endpoint | What it does |
|---|---|---|
| Create | POST `/api/flashcards/{id}/review` | Record a card review (called on Next click) |
| Read | GET `/api/admin/users/{id}/history` | Admin — get a user's full review history |
| Delete | DELETE `/api/admin/users/{id}/history` | Admin — clear a user's history |
| Update | PUT `/api/admin/users/{id}` | Admin — promote or demote a user's admin status |

---

## Challenges I ran into

- SSL certificate error connecting to MongoDB Atlas from Python 3.13 on macOS — `CERTIFICATE_VERIFY_FAILED`. Fixed by installing `certifi` and passing `tlsCAFile=certifi.where()` to the Motor client.
- On the React side, the card index had to reset every time the filter changed, otherwise you'd end up past the end of a shorter list.
- Getting the bookmark icon to fill with a gradient needed a workaround — I defined the gradient once in a hidden SVG in `App.jsx` and referenced it by ID from every bookmark component to match the cotton candy theme.

In part 2, here are some of the issues I faced:
- passlib and bcrypt had a version clash that broke password hashing. Fixed by pinning `bcrypt==4.0.1` and truncating passwords to 72 bytes before hashing since bcrypt silently ignores anything beyond that. (the version is added to requirements.txt)
- Instead of picking a key by hand, used Python's built-in `secrets.token_hex(32)` to generate the JWT signing key properly.
- During testing, found that all flashcard endpoints were publicly accessible without a token — which completely defeats the purpose of adding authentication. Added `dependencies=[Depends(get_current_user)]` to each route decorator to lock them down.
- A naming conflict caught me off guard: a React state variable named `history` silently collides with the browser's built-in `window.history` object, causing a `TypeError: history.map is not a function` at runtime. Renamed it to `reviewHistory` to fix it.


Overall building this end to end was a good learning experience and I actually plan to keep using it to prepare for interviews by adding more custom learning cards in the future.

---

## Team Contributions

| Member | Student ID | Contributions |
|---|---|---|
| Sumangala Somashekhara Rao | 25760517 | Signup/Login, admin panel, testing, error handling |
| Roshan Karthikeya Mahankali | 25762319 | Live search, testing, comments, error handling |