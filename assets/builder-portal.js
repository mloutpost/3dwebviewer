/* ═══════════════════════════════════════════
   Builder & Contractor Portal — JS
   ═══════════════════════════════════════════ */

const BUILDER_PIN = '5000';
const MANIFEST_URL = './assets/manifest.json';
const SESSION_KEY = 'lctf_builder_auth';

// ── State ──
let manifest = null;
let quoteItems = new Map(); // id -> { model, builderPrice, listPrice }

// ── DOM Refs ──
const pinGate = document.getElementById('pin-gate');
const pinInput = document.getElementById('pin-input');
const pinSubmit = document.getElementById('pin-submit');
const pinError = document.getElementById('pin-error');
const portal = document.getElementById('portal');
const grid = document.getElementById('grid');
const searchInput = document.getElementById('q');
const typeFilter = document.getElementById('type-filter');
const discountTier = document.getElementById('discount-tier');
const quoteBar = document.getElementById('quote-bar');
const quoteCount = document.getElementById('quote-count');
const quoteTotal = document.getElementById('quote-total');
const quoteSavings = document.getElementById('quote-savings');

// ════════════════════════════════════════════
// PIN GATE
// ════════════════════════════════════════════

function checkSession() {
  if (sessionStorage.getItem(SESSION_KEY) === 'true') {
    showPortal();
    return true;
  }
  return false;
}

function showPortal() {
  pinGate.classList.add('exiting');
  setTimeout(() => {
    pinGate.style.display = 'none';
    portal.style.display = 'block';
  }, 400);
  loadManifest();
}

function handlePinSubmit() {
  const val = pinInput.value.trim();
  if (val === BUILDER_PIN) {
    sessionStorage.setItem(SESSION_KEY, 'true');
    pinError.style.display = 'none';
    showPortal();
  } else {
    pinError.style.display = 'block';
    pinInput.value = '';
    pinInput.focus();
    // Re-trigger shake
    pinError.style.animation = 'none';
    pinError.offsetHeight; // reflow
    pinError.style.animation = '';
  }
}

pinSubmit.addEventListener('click', handlePinSubmit);
pinInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') handlePinSubmit();
});

document.getElementById('logout-btn').addEventListener('click', () => {
  sessionStorage.removeItem(SESSION_KEY);
  window.location.reload();
});

// ════════════════════════════════════════════
// CATALOG
// ════════════════════════════════════════════

function parsePrice(priceStr) {
  if (!priceStr || priceStr === 'coming soon' || priceStr === 'Call for pricing') return null;
  const num = parseInt(String(priceStr).replace(/[^0-9]/g, ''), 10);
  return isNaN(num) ? null : num;
}

function formatMoney(n) {
  return '$' + n.toLocaleString();
}

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function getDiscount() {
  return parseInt(discountTier.value, 10) || 1500;
}

function getBuilderPrice(listPrice) {
  const discount = getDiscount();
  return Math.max(0, listPrice - discount);
}

function populateTypes(models) {
  const tags = new Set();
  models.forEach(m => { if (m.tag && m.tag !== 'Decorative') tags.add(m.tag); });
  const sorted = Array.from(tags).sort();
  typeFilter.innerHTML = '<option value="">All types</option>';
  sorted.forEach(tag => {
    const opt = document.createElement('option');
    opt.value = tag;
    opt.textContent = tag;
    typeFilter.appendChild(opt);
  });
}

function render() {
  grid.innerHTML = '';
  if (!manifest || !manifest.models) return;

  const q = searchInput.value.trim().toLowerCase();
  const tf = typeFilter.value;
  const discount = getDiscount();

  const filtered = manifest.models.filter(m => {
    // Exclude corbels/decorative items from builder portal
    if (m.tag === 'Decorative') return false;
    if (tf && m.tag !== tf) return false;
    if (q) {
      const hay = ((m.name || '') + ' ' + (m.description || '') + ' ' + (m.tag || '')).toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:3rem;color:var(--text-muted)"><strong>No kits found.</strong><br/>Try adjusting your search or filter.</div>';
    return;
  }

  filtered.forEach(model => {
    const listPrice = parsePrice(model.price);
    const isComingSoon = !listPrice || model.type === 'coming-soon';
    const builderPrice = listPrice ? getBuilderPrice(listPrice) : null;
    const savings = listPrice ? discount : 0;

    const thumbUrl = model.thumbnail
      ? model.thumbnail.replace(/ /g, '%20')
      : 'assets/global_graphics/Small%20Logo%20Cropped.png';

    const card = document.createElement('div');
    card.className = 'p-card' + (isComingSoon ? ' p-card-coming-soon' : '');

    const inQuote = quoteItems.has(model.id);

    card.innerHTML = `
      <div class="p-card-thumb">
        <img src="${thumbUrl}" alt="${escapeHtml(model.name || '')}" loading="lazy"
             onerror="this.src='assets/global_graphics/Small%20Logo%20Cropped.png'" />
      </div>
      <div class="p-card-body">
        <div class="p-card-top">
          <span class="p-card-name">${escapeHtml(model.name || model.id || 'Untitled')}</span>
          ${model.tag ? `<span class="p-card-tag">${escapeHtml(model.tag)}</span>` : ''}
        </div>
        <div class="p-card-pricing">
          ${isComingSoon
        ? '<span style="color:var(--text-muted);font-size:0.85rem">Pricing Coming Soon</span>'
        : `<div class="p-card-price-row">
                <span class="p-price-original">${formatMoney(listPrice)}</span>
                <span class="p-price-builder">${formatMoney(builderPrice)}</span>
                <span class="p-price-saved">Save ${formatMoney(savings)}</span>
              </div>`
      }
        </div>
        ${!isComingSoon ? `
        <div class="p-card-actions">
          <a href="detail.html?id=${encodeURIComponent(model.id)}" class="p-card-view">View Details</a>
          <button class="p-card-quote-btn ${inQuote ? 'added' : ''}" data-id="${escapeHtml(model.id)}">
            ${inQuote ? '✓ In Quote' : '+ Quote'}
          </button>
        </div>` : ''}
      </div>
    `;

    // Quote toggle handler
    const qBtn = card.querySelector('.p-card-quote-btn');
    if (qBtn) {
      qBtn.addEventListener('click', () => {
        toggleQuoteItem(model, listPrice, builderPrice);
      });
    }

    grid.appendChild(card);
  });
}

// ════════════════════════════════════════════
// QUOTE BUILDER
// ════════════════════════════════════════════

function toggleQuoteItem(model, listPrice, builderPrice) {
  if (quoteItems.has(model.id)) {
    quoteItems.delete(model.id);
  } else {
    quoteItems.set(model.id, { model, listPrice, builderPrice });
  }
  updateQuoteBar();
  render(); // re-render to update button states
}

function updateQuoteBar() {
  if (quoteItems.size === 0) {
    quoteBar.style.display = 'none';
    return;
  }
  quoteBar.style.display = 'block';

  let total = 0, savedTotal = 0;
  quoteItems.forEach(item => {
    total += item.builderPrice;
    savedTotal += (item.listPrice - item.builderPrice);
  });

  quoteCount.textContent = quoteItems.size + (quoteItems.size === 1 ? ' kit' : ' kits');
  quoteTotal.textContent = formatMoney(total);
  quoteSavings.textContent = formatMoney(savedTotal);
}

document.getElementById('clear-quote').addEventListener('click', () => {
  quoteItems.clear();
  updateQuoteBar();
  render();
});

document.getElementById('generate-quote').addEventListener('click', showQuoteModal);

function showQuoteModal() {
  const modal = document.getElementById('quote-modal');
  const body = document.getElementById('quote-body');

  let total = 0, listTotal = 0, rebateTotal = 0;
  let rows = '';

  quoteItems.forEach(item => {
    total += item.builderPrice;
    listTotal += item.listPrice;
    const rebate = Math.round(item.builderPrice * 0.01);
    rebateTotal += rebate;
    rows += `
      <tr>
        <td>${escapeHtml(item.model.name || item.model.id)}</td>
        <td class="qt-right"><span class="qt-strike">${formatMoney(item.listPrice)}</span></td>
        <td class="qt-right">${formatMoney(item.builderPrice)}</td>
      </tr>
    `;
  });

  const savedTotal = listTotal - total;
  const today = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const discountLabel = getDiscount() === 3000 ? 'Kits 6+ (−$3,000/kit)' : 'First 5 Kits (−$1,500/kit)';

  body.innerHTML = `
    <div class="quote-brand">
      <img src="assets/global_graphics/LCTF Profile.png" alt="LC Timberframes" />
      <div class="quote-brand-text">
        <h3>LC Timberframes</h3>
        <p>Builder & Contractor Quote</p>
      </div>
    </div>
    <div class="quote-meta">
      <div>Date: ${today}</div>
      <div>Discount Tier: ${discountLabel}</div>
    </div>
    <table class="quote-table">
      <thead>
        <tr>
          <th>Kit</th>
          <th class="qt-right">List Price</th>
          <th class="qt-right">Builder Price</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
    <div class="quote-totals">
      <div class="quote-totals-row">
        <span class="ql">List Total:</span>
        <span>${formatMoney(listTotal)}</span>
      </div>
      <div class="quote-totals-row">
        <span class="ql">Builder Savings:</span>
        <span style="color:var(--accent)">−${formatMoney(savedTotal)}</span>
      </div>
      <div class="quote-totals-row">
        <span class="ql">Est. 1% Rebate:</span>
        <span style="color:var(--gold)">+${formatMoney(rebateTotal)}</span>
      </div>
      <div class="quote-totals-row total">
        <span class="ql">Builder Total:</span>
        <span>${formatMoney(total)}</span>
      </div>
    </div>
    <div class="quote-footer-note">
      Prices are for timber frame kit only and do not include shipping, installation, or additional materials.
      Pricing valid for 30 days from quote date. Contact your LC Timberframes trade representative for final pricing and availability.
    </div>
  `;

  modal.style.display = 'flex';
}

document.getElementById('close-quote-modal').addEventListener('click', () => {
  document.getElementById('quote-modal').style.display = 'none';
});

document.getElementById('print-quote').addEventListener('click', () => {
  window.print();
});

document.getElementById('quote-modal').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) {
    document.getElementById('quote-modal').style.display = 'none';
  }
});

// ════════════════════════════════════════════
// LOAD DATA
// ════════════════════════════════════════════

async function loadManifest() {
  try {
    const res = await fetch(MANIFEST_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    manifest = await res.json();
    if (manifest && manifest.models) {
      populateTypes(manifest.models);
    }
    render();
  } catch (err) {
    grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:3rem;color:var(--text-muted)">
      <strong>Error loading catalog.</strong><br/>${escapeHtml(err.message)}</div>`;
  }
}

// ── Event Listeners ──
searchInput.addEventListener('input', render);
typeFilter.addEventListener('change', render);
discountTier.addEventListener('change', () => {
  // Recalculate quote items with new discount
  quoteItems.forEach((item, id) => {
    item.builderPrice = getBuilderPrice(item.listPrice);
  });
  updateQuoteBar();
  render();
});

// ── Init ──
if (!checkSession()) {
  pinInput.focus();
}
