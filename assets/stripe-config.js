/**
 * Stripe Checkout configuration
 * 
 * To enable Stripe payments:
 * 1. Create a Cloud Function (or API endpoint) that creates Stripe Checkout Sessions
 * 2. Set STRIPE_CHECKOUT_API_URL below to your endpoint
 * 3. Your backend should accept POST with { amount, productId, productName, successUrl, cancelUrl }
 *    and return { url } (the Stripe Checkout URL to redirect to)
 * 
 * Example Firebase Cloud Function (Node.js):
 *   const functions = require('firebase-functions');
 *   const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
 *   exports.createCheckoutSession = functions.https.onCall(async (data) => {
 *     const session = await stripe.checkout.sessions.create({
 *       payment_method_types: ['card', 'us_bank_account', 'apple_pay', 'google_pay'],
 *       line_items: [{ price_data: { currency: 'usd', unit_amount: data.amount, product_data: { name: data.productName } }, quantity: 1 }],
 *       mode: 'payment',
 *       success_url: data.successUrl,
 *       cancel_url: data.cancelUrl,
 *     });
 *     return { url: session.url };
 *   });
 */
window.STRIPE_CONFIG = {
  // Cloud Function in lctf_clients/functions (lctf-projects Firebase)
  checkoutApiUrl: 'https://us-central1-lctf-projects.cloudfunctions.net/createCheckoutSession',
  
  // Stripe publishable key (for Stripe.js - used if you embed Payment Element)
  // Get from https://dashboard.stripe.com/apikeys
  publishableKey: null
};
