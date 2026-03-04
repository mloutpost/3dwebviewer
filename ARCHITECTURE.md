# Architecture: 3dwebviewer + Firebase

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Firebase Project: lctf-projects                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  HOSTING (multiple sites)                    CLOUD FUNCTIONS                 │
│  ┌─────────────────────────────────────┐    ┌──────────────────────────┐   │
│  │  viewer  → shoptimberframekits.com   │    │  createLead              │   │
│  │  clients → clients.lctimberframes   │    │  createCheckoutSession   │   │
│  │  bridges → coveredbridgekits.com    │    │  bridgeCheckout          │   │
│  └─────────────────────────────────────┘    │  bridgeOrderWebhook     │   │
│                                              └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Two Repos, One Deploy

| Repo | Role | What lives here |
|------|------|-----------------|
| **3dwebviewer** | Source of truth for the site | HTML, CSS, JS, manifest, assets. You edit here. |
| **lctf_clients** | Deploy hub | Firebase config, Cloud Functions, symlink to 3dwebviewer |

### How they connect

- `lctf_clients/3dwebviewer` is a **symlink** → `../3dwebviewer`
- `firebase.json` says: hosting target `viewer` uses `public: "3dwebviewer"`
- So when you deploy, Firebase serves the contents of your 3dwebviewer repo

## Deployment Flow

**From 3dwebviewer (recommended):**

```bash
./deploy.sh
```

This deploys both the site and Cloud Functions in one step.

**From lctf_clients (if needed):**

```bash
cd "/Users/lynch/Documents/LCTF Web Builds/lctf_clients"
firebase deploy --only hosting:viewer,functions
```

To deploy only the site or only functions:

```bash
firebase deploy --only hosting:viewer   # site only
firebase deploy --only functions        # functions only
```

## Where things live

| Thing | Location |
|-------|----------|
| Site HTML/CSS/JS | `3dwebviewer/` (this repo) |
| Firebase config | `lctf_clients/firebase.json` |
| Cloud Functions | `lctf_clients/functions/src/index.ts` |
| createLead | `lctf_clients/functions/src/index.ts` |
| bridgeCheckout | `lctf_clients/functions/src/index.ts` |
| createCheckoutSession | To be added in `lctf_clients/functions/src/index.ts` |

## API endpoints (Cloud Functions)

All run in the **lctf-projects** Firebase project:

| Function | URL | Used by |
|----------|-----|---------|
| createLead | `https://us-central1-lctf-projects.cloudfunctions.net/createLead` | claim-kit.html, inquiry.html |
| bridgeCheckout | `https://us-central1-lctf-projects.cloudfunctions.net/bridgeCheckout` | Covered Bridge site |
| createCheckoutSession | `https://us-central1-lctf-projects.cloudfunctions.net/createCheckoutSession` | claim-kit.html (when added) |

## Summary

1. **Edit site** in 3dwebviewer.
2. **Edit functions** in lctf_clients/functions.
3. **Deploy** from lctf_clients: `firebase deploy --only hosting:viewer` for site, `firebase deploy --only functions` for functions.
4. The symlink means 3dwebviewer changes are immediately reflected when you deploy from lctf_clients.
