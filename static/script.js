/* Modern lavender portal script
   - fixed language switching (setLang)
   - floating chat bubble + popup
   - preserves existing flows (categories, services, ai search)
*/

let lang = localStorage.getItem("portal_lang") || "en";
let services = [];        // full services collection (fallback)
let categories = [];
let currentService = null; // store service object when user clicks a subservice
let currentSub = null;
let profile_id = null;
let suggestItems = []; // autosuggest results

/* ----------------------
   Utilities & init
   ---------------------- */
function setLang(l) {
  lang = l;
  localStorage.setItem("portal_lang", l);
  // update active state for buttons
  document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById(`lang-${l}`).classList.add('active');

  // reload UI lists
  loadCategories().then(() => {
    // if we had a current selection, try to re-render it
    if (currentService && currentSub) {
      // find the fresh service object by id (if loaded)
      const svc = services.find(s => s.id === currentService.id);
      if (svc) {
        currentService = svc;
        const sub = (svc.subservices || []).find(s => s.id === currentSub.id);
        if (sub) loadQuestions(svc, sub);
      }
    }
  });
}

/* mark active language button initially */
function initLangUI(){
  document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
  const el = document.getElementById(`lang-${lang}`);
  if(el) el.classList.add('active');
}

/* ----------------------
   Fetch & render: categories
   ---------------------- */
async function loadCategories(){
  try {
    const res = await fetch("/api/categories");
    categories = await res.json();
    const el = document.getElementById("category-list");
    el.innerHTML = "";
    categories.forEach(c => {
      const name = (c.name && (c.name[lang] || c.name.en)) || c.id;
      const btn = document.createElement("div");
      btn.className = "cat-item";
      btn.textContent = name;
      btn.onclick = () => loadMinistriesInCategory(c);
      el.appendChild(btn);
    });
    // also refresh ads
    loadAds();
  } catch (err) {
    console.error("Failed to load categories", err);
  }
}

/* load ministries/services for a category */
async function loadMinistriesInCategory(cat){
  document.getElementById("sub-list").innerHTML = "";
  document.getElementById("sub-title").innerText = (cat.name && (cat.name[lang] || cat.name.en)) || cat.id;

  // pick ministry ids if present
  if (cat.ministry_ids && cat.ministry_ids.length) {
    for (let id of cat.ministry_ids) {
      const r = await fetch(`/api/service/${id}`);
      const s = await r.json();
      if (s && s.subservices) {
        s.subservices.forEach(sub => {
          const li = document.createElement("li");
          li.textContent = (sub.name && (sub.name[lang] || sub.name.en)) || sub.id;
          li.onclick = () => loadQuestions(s, sub);
          document.getElementById("sub-list").appendChild(li);
        });
      }
    }
  } else {
    // fallback: load all services (cache into services var)
    if (!services.length) {
      const srv = await fetch("/api/services");
      services = await srv.json();
    }
    const filtered = services.filter(s => s.category === cat.id);
    filtered.forEach(s => {
      (s.subservices || []).forEach(sub => {
        const li = document.createElement("li");
        li.textContent = (sub.name && (sub.name[lang] || sub.name.en)) || sub.id;
        li.onclick = () => loadQuestions(s, sub);
        document.getElementById("sub-list").appendChild(li);
      });
    });
  }
}

/* ----------------------
   Questions and answers
   ---------------------- */
async function loadQuestions(service, sub){
  // ensure we store objects for re-render on language change
  currentService = service;
  currentSub = sub;

  currentServiceName = (service.name && (service.name[lang] || service.name.en)) || service.id;
  const qList = document.getElementById("question-list");
  qList.innerHTML = "";
  document.getElementById("q-title").innerText = (sub.name && (sub.name[lang] || sub.name.en)) || sub.id;

  (sub.questions || []).forEach(q => {
    const li = document.createElement("li");
    li.textContent = (q.q && (q.q[lang] || q.q.en)) || q.q || "Untitled";
    li.onclick = () => showAnswer(service, sub, q);
    qList.appendChild(li);
  });
}

function showAnswer(service, sub, q){
  let html = `<h3>${(q.q && (q.q[lang] || q.q.en)) || q.q}</h3>`;
  html += `<p>${(q.answer && (q.answer[lang] || q.answer.en)) || q.answer || ""}</p>`;
  if (q.downloads && q.downloads.length){
    html += `<p><b>Downloads:</b> ${q.downloads.map(d=>`<a href="${d}" target="_blank">${d.split("/").pop()}</a>`).join(", ")}</p>`;
  }
  if (q.location){
    html += `<p><b>Location:</b> <a href="${q.location}" target="_blank">View Map</a></p>`;
  }
  if (q.instructions){
    html += `<p><b>Instructions:</b> ${q.instructions}</p>`;
  }
  document.getElementById("answer-box").innerHTML = html;

  // log engagement
  fetch("/api/engagement", {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      user_id: profile_id, age:null, job:null, desires: [], question_clicked: (q.q && (q.q[lang] || q.q.en)) || q.q, service: (service.name && (service.name[lang] || service.name.en)) || service.id
    })
  });
}

/* ----------------------
   Ads + officers (small)
   ---------------------- */
async function loadAds(){
  try {
    const res = await fetch("/api/ads");
    const ads = await res.json();
    const el = document.getElementById("ads-area");
    el.innerHTML = ads.map(a => `<div class="ad-card"><a href="${a.link||'#'}"><strong>${a.title}</strong><div style="font-size:13px;color:var(--muted)">${a.body||''}</div></a></div>`).join("");
  } catch(e){ console.warn("ads load error", e); }
}

/* ----------------------
   Autosuggest (search & chat)
   ---------------------- */
let suggestTimer = null;
async function autosuggest(q){
  clearTimeout(suggestTimer);
  const suggestionsEl = document.getElementById("suggestions");
  if(!q || q.length < 2){ suggestionsEl.innerHTML = ""; return; }
  suggestTimer = setTimeout(async ()=>{
    try {
      const res = await fetch(`/api/search/autosuggest?q=${encodeURIComponent(q)}`);
      const items = await res.json();
      suggestItems = items || [];
      suggestionsEl.innerHTML = suggestItems.map((it, idx) => `<div class="s-item" data-idx="${idx}">${(it.name && (it.name[lang] || it.name.en)) || it.name || it.id}</div>`).join("");
      // attach listeners
      suggestionsEl.querySelectorAll('.s-item').forEach(el=>{
        el.onclick = ()=> {
          const idx = el.getAttribute('data-idx');
          const it = suggestItems[parseInt(idx)];
          pickSuggestion(it);
        };
      });
    } catch (err) {
      console.error("autosuggest error", err);
    }
  }, 220);
}

function pickSuggestion(it){
  if(!it) return;
  // if suggestion has subservices, open first
  if(it.subservices && it.subservices.length){
    loadQuestions(it, it.subservices[0]);
  } else {
    // else try search the AI
    openChat();
    document.getElementById("chat-text").value = (it.name && (it.name[lang] || it.name.en)) || it.name || "";
  }
  document.getElementById("suggestions").innerHTML = "";
}

/* ----------------------
   Floating Chat UI
   ---------------------- */
const chatToggle = document.getElementById("chat-toggle");
const chatPopup = document.getElementById("chat-popup");
const chatBody = document.getElementById("chat-body");

chatToggle.addEventListener('click', () => {
  // toggle
  if (chatPopup.classList.contains('open')) closeChat();
  else openChat();
});

function openChat(){
  chatPopup.classList.add('open');
  chatPopup.setAttribute('aria-hidden','false');
  // focus input
  setTimeout(()=> document.getElementById('chat-text').focus(), 180);
}

function closeChat(){
  chatPopup.classList.remove('open');
  chatPopup.setAttribute('aria-hidden','true');
}

/* sendChat / append chat */
async function sendChat(){
  const input = document.getElementById("chat-text");
  const text = input.value && input.value.trim();
  if(!text) return;
  appendChat("user", text);
  input.value = "";
  // call ai endpoint
  try {
    const res = await fetch("/api/ai/search", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({query: text, top_k: 5})
    });
    const data = await res.json();
    const reply = (data && data.answer) ? data.answer : "No answer found.";
    appendChat("bot", reply);
  } catch (err) {
    appendChat("bot", "Error contacting AI. Try again later.");
    console.error(err);
  }

  // log engagement
  fetch("/api/engagement", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({user_id: profile_id, question_clicked: text, service: null})
  });
}

function appendChat(sender, text){
  const div = document.createElement("div");
  div.className = `chat-msg ${sender === "user" ? "user-msg" : "bot-msg"}`;
  div.innerText = text;
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}

/* Close chat when clicking outside */
document.addEventListener('click', (ev) => {
  const target = ev.target;
  if (!chatPopup.contains(target) && !chatToggle.contains(target) && chatPopup.classList.contains('open')) {
    closeChat();
  }
});

/* ----------------------
   Profile modal & steps (kept minimal)
   ---------------------- */
async function profileSubmit(){ /* kept minimal in redesign - existing endpoint used by profile modal if shown */ }

/* ----------------------
   Init on load
   ---------------------- */
window.onload = async () => {
  initLangUI();
  await loadCategories();
  // load services fallback
  try {
    const r = await fetch("/api/services");
    services = await r.json();
  } catch(e){ console.warn("services load failed", e); }

  // small UX: wire search input enter to open chat with value
  const search = document.getElementById("search-input");
  search.addEventListener('keydown', (e) => {
    if(e.key === 'Enter'){
      const v = search.value && search.value.trim();
      if(v) {
        openChat();
        document.getElementById('chat-text').value = v;
        sendChat();
      }
    }
  });
};
