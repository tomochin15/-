
const SETTINGS_KEY = 'pokeka_authority_alerts_v1';
const POLL_INTERVAL = 60 * 1000;
const AMAZON_TAG = 'YOUR_AMAZON_ASSOCIATE_ID';
const RAKUTEN_AFFILIATE_URL = 'https://hb.afl.rakuten.co.jp/';
const YAHOO_AFFILIATE_URL = 'https://shopping.yahoo.co.jp/';
let lastSignature = '';

async function fetchData(){
  const r = await fetch(`data.json?ts=${Date.now()}`);
  return r.json();
}
function parseDate(v){
  if(!v || v === '未定' || v === '未発表') return null;
  const d = new Date(v.replace(' ','T'));
  return Number.isNaN(d.getTime()) ? null : d;
}
function formatDate(v){
  const d = parseDate(v);
  return d ? d.toLocaleString('ja-JP') : (v || '未定');
}
function statusClass(v=''){
  if(v.includes('受付中')) return 'status-open';
  if(v.includes('予告') || v.includes('監視中') || v.includes('告知待ち')) return 'status-soon';
  if(v.includes('終了')) return 'status-closed';
  return '';
}
function signature(d){ return JSON.stringify(d); }
function sortByPublished(items){
  return [...items].sort((a,b)=>(parseDate(b.publishedAt)?.getTime()||0)-(parseDate(a.publishedAt)?.getTime()||0));
}
function countdownText(end){
  const d = parseDate(end);
  if(!d) return '未定';
  const diff = d.getTime() - Date.now();
  if(diff <= 0) return '終了';
  const h = Math.floor(diff / 3600000);
  const day = Math.floor(h / 24);
  const rem = h % 24;
  return day > 0 ? `あと${day}日${rem}時間` : `あと${h}時間`;
}
function buildLatest(data){
  const lottery = (data.lottery||[]).map(x => ({...x, typeLabel:'抽選', pageType:'lottery', title:x.product}));
  const commerce = (data.commerce||[]).map(x => ({...x, typeLabel:x.kind || '販売', pageType:'commerce'}));
  const social = (data.social||[]).map(x => ({...x, typeLabel:'X情報', pageType:'social'}));
  return sortByPublished([...lottery, ...commerce, ...social]);
}
function renderStats(data){
  const set = (id,val) => { const el = document.getElementById(id); if(el) el.textContent = val; };
  set('updatedAt', formatDate(data.site.updatedAt));
  set('statLottery', String((data.lottery||[]).length));
  set('statOpen', String((data.lottery||[]).filter(x => (x.status||'').includes('受付中')).length));
  set('statCommerce', String((data.commerce||[]).length));
  set('statSocial', String((data.social||[]).length));
}
function renderLatest(data){
  const el = document.getElementById('latestFeed');
  if(!el) return;
  el.innerHTML = '';
  buildLatest(data).forEach(item => {
    const article = document.createElement('article');
    article.className = 'feed-item';
    article.dataset.shop = item.shop || item.source || '';
    const tagClass = item.pageType === 'lottery' ? 'lottery' : item.pageType === 'commerce' ? 'commerce' : 'social';
    const shop = item.shop || item.source || '';
    const summary = item.summary || '';
    const status = item.status ? `<p class="${statusClass(item.status)}">${item.status}</p>` : '';
    article.innerHTML = `
      <div class="meta">
        <span class="tag ${tagClass}">${item.typeLabel}</span>
        <span>${shop}</span>
        <span>${formatDate(item.publishedAt)}</span>
      </div>
      <h3>${item.title}</h3>
      ${status}
      ${summary ? `<p>${summary}</p>` : ''}
      <a href="${item.url}" target="_blank" rel="noopener noreferrer">リンクを開く</a>
    `;
    el.appendChild(article);
  });
}
function renderLottery(data){
  const tbody = document.querySelector('#lotteryTable tbody');
  if(!tbody) return;
  tbody.innerHTML = '';
  sortByPublished(data.lottery||[]).forEach(item => {
    const tr = document.createElement('tr');
    tr.dataset.shop = item.shop;
    tr.dataset.status = item.status || '';
    tr.innerHTML = `
      <td>${item.shop}</td>
      <td>${item.product}</td>
      <td class="${statusClass(item.status)}">${item.status}</td>
      <td>${formatDate(item.start)} ～ ${formatDate(item.end)}</td>
      <td>${item.result ? formatDate(item.result) : '-'}</td>
      <td><span class="countdown">${countdownText(item.end)}</span></td>
      <td><a href="${item.url}" target="_blank" rel="noopener noreferrer">公式へ</a></td>
    `;
    tbody.appendChild(tr);
  });
}
function renderCommerce(data){
  const el = document.getElementById('commerceFeed');
  if(!el) return;
  el.innerHTML = '';
  sortByPublished(data.commerce||[]).forEach(item => {
    const card = document.createElement('article');
    card.className = 'feed-item';
    card.innerHTML = `
      <div class="meta">
        <span class="tag commerce">${item.kind || '販売'}</span>
        <span>${item.shop}</span>
        <span>${formatDate(item.publishedAt)}</span>
      </div>
      <h3>${item.title}</h3>
      <p class="${statusClass(item.status)}">${item.status}</p>
      <p>${item.summary || ''}</p>
      <a href="${item.url}" target="_blank" rel="noopener noreferrer">リンクを開く</a>
    `;
    el.appendChild(card);
  });
}
function renderSocial(data){
  const el = document.getElementById('socialFeed');
  if(!el) return;
  el.innerHTML = '';
  sortByPublished(data.social||[]).forEach(item => {
    const card = document.createElement('article');
    card.className = 'feed-item';
    card.innerHTML = `
      <div class="meta">
        <span class="tag social">X情報</span>
        <span>${item.source}</span>
        <span>${formatDate(item.publishedAt)}</span>
      </div>
      <h3>${item.title}</h3>
      <p>${item.summary || ''}</p>
      <a href="${item.url}" target="_blank" rel="noopener noreferrer">リンクを開く</a>
    `;
    el.appendChild(card);
  });
}
function renderCalendar(data){
  const el = document.getElementById('calendarFeed');
  if(!el) return;
  el.innerHTML = '';
  const events = [];
  (data.lottery||[]).forEach(item => {
    if(item.start && item.start !== '未定') events.push({date:item.start, label:'抽選開始', shop:item.shop, product:item.product, url:item.url});
    if(item.end && item.end !== '未定') events.push({date:item.end, label:'応募締切', shop:item.shop, product:item.product, url:item.url});
    if(item.result && item.result !== '未定') events.push({date:item.result, label:'結果発表', shop:item.shop, product:item.product, url:item.url});
  });
  events.sort((a,b)=>(parseDate(a.date)?.getTime()||0)-(parseDate(b.date)?.getTime()||0));
  events.forEach(item => {
    const card = document.createElement('article');
    card.className = 'feed-item';
    card.innerHTML = `
      <div class="meta">
        <span class="tag calendar">${item.label}</span>
        <span>${item.shop}</span>
        <span>${formatDate(item.date)}</span>
      </div>
      <h3>${item.product}</h3>
      <a href="${item.url}" target="_blank" rel="noopener noreferrer">公式ページ</a>
    `;
    el.appendChild(card);
  });
}
function renderShops(data){
  const el = document.getElementById('shopFeed');
  if(!el) return;
  el.innerHTML = '';
  (data.shops||[]).forEach(item => {
    const card = document.createElement('article');
    card.className = 'feed-item';
    card.innerHTML = `
      <div class="meta">
        <span class="shop-badge">${item.type}</span>
        <span class="shop-badge">${item.priority}</span>
      </div>
      <h3>${item.name}</h3>
      <p>${item.strength}</p>
    `;
    el.appendChild(card);
  });
}
function renderFaq(data){
  const el = document.getElementById('faqFeed');
  if(!el) return;
  el.innerHTML = '';
  (data.faq||[]).forEach(item => {
    const div = document.createElement('div');
    div.className = 'faq-item';
    div.innerHTML = `<strong>${item.q}</strong><p>${item.a}</p>`;
    el.appendChild(div);
  });
}
function renderGuides(data){
  const el = document.getElementById('guideFeed');
  if(!el) return;
  el.innerHTML = '';
  (data.guides||[]).forEach(item => {
    const card = document.createElement('article');
    card.className = 'feed-item';
    card.innerHTML = `<h3>${item.title}</h3><p>${item.desc}</p><a href="${item.url}">ガイドを見る</a>`;
    el.appendChild(card);
  });
}
function allShops(data){
  const s = new Set();
  (data.lottery||[]).forEach(x => s.add(x.shop));
  (data.commerce||[]).forEach(x => s.add(x.shop));
  return [...s].sort();
}
function defaults(shops){
  return {
    enableStartAlert: true,
    enableDeadlineAlert: true,
    deadlineLead: '24',
    shops: Object.fromEntries(shops.map(s => [s, true])),
    seenStarts: {},
    seenDeadlines: {}
  };
}
function loadSettings(shops){
  const raw = JSON.parse(localStorage.getItem(SETTINGS_KEY) || 'null');
  const base = defaults(shops);
  if(!raw) return base;
  return {
    ...base,
    ...raw,
    shops: { ...base.shops, ...(raw.shops || {}) },
    seenStarts: raw.seenStarts || {},
    seenDeadlines: raw.seenDeadlines || {}
  };
}
function saveSettings(settings){
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}
function renderAlertSettings(data){
  const shops = allShops(data);
  const settings = loadSettings(shops);
  const shopBox = document.getElementById('shopToggles');
  if(shopBox){
    shopBox.innerHTML = '';
    shops.forEach(shop => {
      const label = document.createElement('label');
      label.className = 'toggle-card';
      label.innerHTML = `<input type="checkbox" data-shop="${shop}" ${settings.shops[shop] ? 'checked' : ''}> ${shop}`;
      shopBox.appendChild(label);
    });
  }
  const s = document.getElementById('enableStartAlert');
  const d = document.getElementById('enableDeadlineAlert');
  const lead = document.getElementById('deadlineLead');
  if(s) s.checked = settings.enableStartAlert;
  if(d) d.checked = settings.enableDeadlineAlert;
  if(lead) lead.value = settings.deadlineLead;
  return settings;
}
function currentSettings(prev){
  const out = structuredClone(prev);
  const s = document.getElementById('enableStartAlert');
  const d = document.getElementById('enableDeadlineAlert');
  const lead = document.getElementById('deadlineLead');
  if(s) out.enableStartAlert = s.checked;
  if(d) out.enableDeadlineAlert = d.checked;
  if(lead) out.deadlineLead = lead.value;
  document.querySelectorAll('#shopToggles input[type="checkbox"]').forEach(input => {
    out.shops[input.dataset.shop] = input.checked;
  });
  return out;
}
async function askNotification(){
  if(!('Notification' in window)){
    alert('このブラウザは通知に対応していません。');
    return;
  }
  const result = await Notification.requestPermission();
  if(result === 'granted') alert('通知を許可しました。');
}
function fireNotice(title, body){
  if(!('Notification' in window) || Notification.permission !== 'granted') return;
  new Notification(title, { body });
}
function evaluateAlerts(data, settings){
  const now = new Date();
  const lead = Number(settings.deadlineLead || '24');
  (data.lottery||[]).forEach(item => {
    if(!settings.shops[item.shop]) return;
    const start = parseDate(item.start);
    const end = parseDate(item.end);
    if(settings.enableStartAlert && start && now >= start){
      const key = `${item.shop}__${item.product}__${item.start}`;
      if(!settings.seenStarts[key]){
        settings.seenStarts[key] = true;
        fireNotice(`抽選開始: ${item.shop}`, `${item.product} の受付が始まりました。`);
      }
    }
    if(settings.enableDeadlineAlert && end){
      const hours = (end.getTime() - now.getTime()) / 3600000;
      const key = `${item.shop}__${item.product}__${item.end}__${lead}`;
      if(hours <= lead && hours > 0 && !settings.seenDeadlines[key]){
        settings.seenDeadlines[key] = true;
        fireNotice(`締切前: ${item.shop}`, `${item.product} の締切が ${lead}時間以内です。`);
      }
    }
  });
  saveSettings(settings);
}
function fillFilters(data){
  const shopFilter = document.getElementById('shopFilter');
  if(shopFilter){
    shopFilter.innerHTML = `<option value="">すべてのショップ</option>` + allShops(data).map(s => `<option value="${s}">${s}</option>`).join('');
  }
}
function applyFilters(){
  const keyword = (document.getElementById('searchBox')?.value || '').toLowerCase().trim();
  const shop = document.getElementById('shopFilter')?.value || '';
  const status = document.getElementById('statusFilter')?.value || '';
  document.querySelectorAll('#lotteryTable tbody tr').forEach(row => {
    const text = row.textContent.toLowerCase();
    const rowShop = row.dataset.shop || '';
    const rowStatus = row.dataset.status || '';
    const show = (!keyword || text.includes(keyword)) && (!shop || rowShop === shop) && (!status || rowStatus.includes(status));
    row.style.display = show ? '' : 'none';
  });
  document.querySelectorAll('#latestFeed .feed-item').forEach(card => {
    const text = card.textContent.toLowerCase();
    const cardShop = card.dataset.shop || '';
    const show = (!keyword || text.includes(keyword)) && (!shop || cardShop === shop);
    card.style.display = show ? '' : 'none';
  });
}
function updateAffiliateLinks(){
  const amazon = document.getElementById('amazonLink');
  const rakuten = document.getElementById('rakutenLink');
  const yahoo = document.getElementById('yahooLink');
  if(amazon){
    amazon.href = `https://www.amazon.co.jp/s?k=${encodeURIComponent('ポケモンカード')}&tag=${encodeURIComponent(AMAZON_TAG)}`;
  }
  if(rakuten) rakuten.href = RAKUTEN_AFFILIATE_URL;
  if(yahoo) yahoo.href = YAHOO_AFFILIATE_URL;
}
async function renderAll(){
  const data = await fetchData();
  renderStats(data);
  renderLatest(data);
  renderLottery(data);
  renderCommerce(data);
  renderSocial(data);
  renderCalendar(data);
  renderShops(data);
  renderFaq(data);
  renderGuides(data);
  fillFilters(data);
  updateAffiliateLinks();
  let settings = renderAlertSettings(data);
  evaluateAlerts(data, settings);
  lastSignature = signature(data);
  document.getElementById('notifyPermissionBtn')?.addEventListener('click', askNotification);
  document.getElementById('saveSettingsBtn')?.addEventListener('click', () => {
    settings = currentSettings(settings);
    saveSettings(settings);
    alert('設定を保存しました。');
  });
  document.getElementById('searchBox')?.addEventListener('input', applyFilters);
  document.getElementById('shopFilter')?.addEventListener('change', applyFilters);
  document.getElementById('statusFilter')?.addEventListener('change', applyFilters);
}
async function poll(){
  try{
    const data = await fetchData();
    const sig = signature(data);
    if(sig !== lastSignature){
      renderStats(data);
      renderLatest(data);
      renderLottery(data);
      renderCommerce(data);
      renderSocial(data);
      renderCalendar(data);
      renderShops(data);
      renderFaq(data);
      renderGuides(data);
      fillFilters(data);
      let settings = renderAlertSettings(data);
      evaluateAlerts(data, settings);
      applyFilters();
      lastSignature = sig;
    }
  }catch(e){
    console.error(e);
  }
}
document.addEventListener('DOMContentLoaded', async () => {
  await renderAll();
  setInterval(poll, POLL_INTERVAL);
});
