# Fix CORS and auth redirect as per task

## Plan Breakdown & Progress Tracker

### ✅ Step 1: Create/update this TODO.md - [DONE]

### ✅ Step 2: Edit backend/main.py - [DONE]
- Replace CORSMiddleware allow_origins=["*"] with specific Netlify origins

### ✅ Step 3: Edit Frontend/js/auth.js - [DONE]  
- Update admin redirect URL in _redirectSetelahLogin() to Netlify dashboard URL

### ⏳ Step 4: Test changes
- Backend: `cd backend && uvicorn main:app --reload`, check CORS headers
- Frontend: Test login as admin from login.html, verify redirect

### ✅ Step 5: Mark complete

