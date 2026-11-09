# PBT Shifts & Pay

Shift calendar and pay calculator for DP World Port Botany VSEs (DP World Sydney Enterprise Agreement 2024).

- **Open / install the app:** https://shipwreckbay123.github.io/pbt-shifts/
  - Android: open in Chrome → ⋮ → *Install app*
  - iPhone: open in Safari → Share → *Add to Home Screen*
- **Android install file:** https://github.com/shipwreckbay123/pbt-shifts/releases/latest/download/pbt-shifts.apk

Everyone's shifts and payslips are saved on their own phone only. Nothing personal is stored in this repo.

This is a personal test app, not an official DP World tool. Always check your payslip.

## How it's built
- `index.html` is the whole app. Pushing to `main` republishes it (`.github/workflows/pages.yml`).
- `android-shell/` is a Capacitor wrapper that opens the hosted app. Changes there build a new signed APK
  (`.github/workflows/apk.yml`), using the `ANDROID_KEYSTORE_B64` and `ANDROID_KEYSTORE_PASSWORD` secrets.
  Keep the same key, or phones can't update the app.

## Crew chat (Firebase)
The Chat tab uses Firebase: anonymous sign-in plus a Firestore collection `rooms/main/messages` ({uid, name, text, ts}).
- Fill in `FIREBASE_CONFIG` in `index.html` with the web app config from the Firebase console. Until then the tab says the chat isn't switched on.
- Turn on **Authentication → Sign-in method → Anonymous**, create a **Firestore** database (Sydney, australia-southeast1), and paste `firestore.rules` into Firestore → Rules.
- `vendor/firebase-chat.js` is Firebase JS SDK 11.10 (app, auth, firestore) bundled with esbuild from a small entry file that only exports what the chat uses.
- Anyone can delete their own messages. To remove someone else's, delete it in the Firebase console.
- Phone notifications are not built yet: they need Firebase's Blaze plan (Cloud Functions) and only work for Chrome / iPhone home-screen installs, not inside the APK.
