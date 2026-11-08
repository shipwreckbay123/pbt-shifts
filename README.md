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
