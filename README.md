# System Design Flashcards

A flashcard web app to help study system design concepts, built as part of Assignment 1 for the Web Development course. The app lets you flip through cards one at a time, bookmark the ones you want to revisit, and manage your own card library.

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

Here's roughly how it all connects:

```
Browser (React on port 5173)
        ↕  Axios (HTTP requests)
FastAPI server (Python on port 8000)
        ↕  Motor async driver
MongoDB Atlas (cloud database)
```

---

## Features

- Single page app — no reloads, React handles everything dynamically
- One card shown at a time — click to flip, then hit Next to move on
- 101 pre-loaded system design cards across Easy, Medium, and Hard
- Filter cards by difficulty (All / Easy / Medium / Hard)
- Bookmark cards with the bookmark icon to save them for later
- Filter by favourites to review only bookmarked cards
- Add your own flashcards with question, answer, category and difficulty
- Edit any card — changes take effect immediately and reset the deck
- Delete cards you don't need anymore
- Progress bar tracks how many cards you've reviewed vs how many are left
- Reset button to start the deck over
- Works on mobile too
- If the backend goes down, the app shows an error message instead of a blank screen

---

## Folder Structure

```
flashcard-app/
├── README.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app + CORS setup
│   │   ├── database.py              # MongoDB connection
│   │   ├── models/
│   │   │   └── flashcard.py         # Data shape for create / update / response
│   │   └── routes/
│   │       └── flashcardAPIs.py     # All the CRUD endpoints
│   ├── seed.py                      # Run once to load 101 cards into the DB
│   ├── requirements.txt
│   └── .env                         # MongoDB URL — not committed to GitHub
└── frontend/
    └── src/
        ├── components/
        │   ├── BookmarkIcon.jsx      # SVG bookmark icon (outline or filled)
        │   ├── FlashcardDeck.jsx     # Main component that manages everything
        │   ├── FlashcardCard.jsx     # The actual card with flip animation
        │   ├── FilterBar.jsx         # Difficulty + favourites filter buttons
        │   ├── ProgressBar.jsx       # Shows reviewed vs remaining
        │   ├── AddCardModal.jsx      # Form to create a new card
        │   └── EditCardModal.jsx     # Form to edit an existing card
        ├── hooks/
        │   └── useFlashcards.js      # Custom hook that handles all data and state
        ├── services/
        │   └── api.js                # All axios calls live here, nowhere else
        ├── App.jsx
        └── index.css                 # All the styling
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
```

Load the flashcards into the database:
```bash
python3 seed.py
```

Start the server:
```bash
uvicorn app.main:app --reload
```

You can test and read the documentation for all the API endpoints at `http://localhost:8000/docs` — FastAPI open API specs

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` and it should work.

---

## CRUD operations

| Operation | Endpoint | What it does |
|---|---|---|
| Create | POST `/api/flashcards/` | Add a new card |
| Read | GET `/api/flashcards/` | Get all cards (can filter by difficulty or favourite) |
| Read | GET `/api/flashcards/{id}` | Get one card |
| Update | PUT `/api/flashcards/{id}` | Edit a card or toggle bookmark |
| Delete | DELETE `/api/flashcards/{id}` | Delete a card (returns 204) |

---

## Challenges I ran into

- The first big issue was an SSL certificate error when trying to connect to MongoDB Atlas from Python 3.13 on macOS — the error was `CERTIFICATE_VERIFY_FAILED` and it took a while to figure out. The fix was installing the `certifi` package and passing `tlsCAFile=certifi.where()` to the Motor client. 
- On the React side, managing which card to show was trickier than expected because the index had to reset every time the filter changed, otherwise you'd end up past the end of a shorter list. 
- Getting the bookmark icon to fill with a gradient also needed a bit of a workaround coz I wanted to match it with the cotton candy like theme, I had set for the add, I defined the gradient once in a hidden SVG in `App.jsx` and referenced it by ID from every bookmark component.
Overall though building this end to end was a good learning experience and I actually plan to keep using it to prepare for my interviews in the future.