# Firebase Authentication Setup Guide

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: `mirmer-ai` (or your preferred name)
4. Disable Google Analytics (optional for MVP)
5. Click "Create project"

## Step 2: Enable Google Authentication

1. In your Firebase project, go to **Authentication** in the left sidebar
2. Click "Get started"
3. Go to the **Sign-in method** tab
4. Click on **Google**
5. Toggle "Enable"
6. Select a support email
7. Click "Save"

## Step 3: Register Your Web App

1. In Project Overview, click the **Web icon** (`</>`)
2. Register app name: `Mirmer AI Web`
3. Click "Register app"
4. Copy the Firebase configuration object

## Step 4: Configure Your App

1. Create `frontend/.env` file (copy from `frontend/.env.example`)
2. Fill in your Firebase credentials:

```env
VITE_FIREBASE_API_KEY=AIzaSy...
VITE_FIREBASE_AUTH_DOMAIN=mirmer-ai-xxxxx.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=mirmer-ai-xxxxx
VITE_FIREBASE_STORAGE_BUCKET=mirmer-ai-xxxxx.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:xxxxx
```

## Step 5: Configure Authorized Domains

1. In Firebase Console, go to **Authentication** → **Settings** → **Authorized domains**
2. Add your domains:
   - `localhost` (already added by default)
   - Your production domain (e.g., `mirmer-ai.vercel.app`)

## Step 6: Test Authentication

1. Start your app: `./start.sh`
2. Open http://localhost:5173
3. Click "Continue with Google"
4. Sign in with your Google account
5. You should be redirected to the main app!

## Security Rules (Optional but Recommended)

### Firestore Rules (if you add Firestore later)
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /conversations/{conversationId} {
      allow read, write: if request.auth != null && 
        resource.data.userId == request.auth.uid;
    }
  }
}
```

## Next Steps

- [ ] Set up Firebase project
- [ ] Enable Google Authentication
- [ ] Add Firebase credentials to `.env`
- [ ] Test login flow
- [ ] (Optional) Add more auth providers (Email/Password, GitHub, etc.)
- [ ] (Optional) Set up Firestore for cloud storage instead of local JSON

## Troubleshooting

**Error: "Firebase: Error (auth/unauthorized-domain)"**
- Add your domain to Authorized domains in Firebase Console

**Error: "Firebase: Error (auth/popup-blocked)"**
- Allow popups in your browser for localhost

**Error: "Firebase: Error (auth/configuration-not-found)"**
- Check that all environment variables are set correctly in `.env`
