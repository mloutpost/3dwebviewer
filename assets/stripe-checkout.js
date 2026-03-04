/**
 * Stripe Checkout - redirects to Stripe-hosted payment page
 * Requires STRIPE_CONFIG.checkoutApiUrl to be set and backend to create Checkout Sessions
 */
(function() {
  'use strict';

  window.redirectToStripeCheckout = async function(options) {
    const config = window.STRIPE_CONFIG || {};
    const apiUrl = config.checkoutApiUrl;

    if (!apiUrl) {
      console.warn('Stripe: checkoutApiUrl not configured. Set STRIPE_CONFIG.checkoutApiUrl in assets/stripe-config.js');
      return false;
    }

    const {
      amount = 0,           // in cents
      productId = '',
      productName = 'Timber Frame Kit',
      successUrl = window.location.origin + '/index.html?payment=success',
      cancelUrl = window.location.href
    } = options || {};

    if (!amount || amount < 50) {
      console.error('Stripe: amount must be at least 50 cents');
      return false;
    }

    try {
      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount,
          productId,
          productName,
          successUrl,
          cancelUrl
        })
      });

      if (!res.ok) {
        throw new Error('Failed to create checkout session');
      }

      const data = await res.json();
      if (data.url) {
        window.location.href = data.url;
        return true;
      }
      throw new Error('No checkout URL returned');
    } catch (err) {
      console.error('Stripe checkout error:', err);
      return false;
    }
  };
})();
