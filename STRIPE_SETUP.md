# Stripe Payment Integration Setup

The site displays accepted payment methods (credit cards, ACH, Apple Pay, Google Pay) and includes a Stripe Checkout flow.

## Architecture

- **Frontend**: 3dwebviewer (this repo) — `claim-kit.html` calls the checkout API
- **Backend**: lctf_clients/functions — `createCheckoutSession` Cloud Function
- **Firebase project**: lctf-projects (same as createLead, bridgeCheckout)

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full deployment flow.

## 1. Stripe configuration

The `createCheckoutSession` function uses the same Stripe config as `bridgeCheckout`:

```bash
cd "/Users/lynch/Documents/LCTF Web Builds/lctf_clients"
firebase functions:config:get stripe
```

You should see `stripe.secret_key`. If not:

```bash
firebase functions:config:set stripe.secret_key="sk_live_..."
```

## 2. Deploy

From the 3dwebviewer repo:

```bash
./deploy.sh
```

This deploys both the site and functions.

## 4. Payment flow

- **claim-kit.html**: "Pay $500 deposit now" → POST to createCheckoutSession → redirect to Stripe
- **Success**: User returns to `claim-kit.html?payment=success`
- **Cancel**: User returns to claim-kit page

## Accepted payment methods

The Checkout Session is configured for:
- **Cards**: Visa, Mastercard, Amex, Discover
- **ACH**: US bank transfers
- **Apple Pay** / **Google Pay**: Shown when available
