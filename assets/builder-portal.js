/* ═══════════════════════════════════════════
   Builder & Contractor Portal — JS
   ═══════════════════════════════════════════ */

const BUILDER_PIN = '5000';
const MANIFEST_URL = './assets/manifest.json';
const SESSION_KEY = 'lctf_builder_auth';

// ── State ──
let manifest = null;

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
        </div>` : ''}
      </div>
    `;

    grid.appendChild(card);
  });
}



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
discountTier.addEventListener('change', render);

// ── Init ──
if (!checkSession()) {
  pinInput.focus();
}
