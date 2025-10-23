let lang = localStorage.getItem("portal_lang") || "en";
let services = [];
let categories = [];
let currentServiceName = "";
let currentSub = null;
let profile_id = null;

/* ---------------------------
   INITIAL LOAD
--------------------------- */
document.addEventListener("DOMContentLoaded", async () => {
  await loadCategories();
  await loadAds();
  await loadServices();

  lucide.createIcons(); // ensure icons are rendered before anything else

  // Restore theme
  const savedTheme = localStorage.getItem("portal_theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark");
  }
  updateThemeIcon(document.body.classList.contains("dark"));

  // Listeners
  const themeBtn = document.getElementById("theme-toggle");
  if (themeBtn) themeBtn.addEventListener("click", toggleTheme);

  const chatFloat = document.getElementById("chat-float");
  const chatClose = document.getElementById("chat-close");
  const chatOverlay = document.getElementById("chat-overlay");
  if (chatFloat) chatFloat.addEventListener("click", openChat);
  if (chatClose) chatClose.addEventListener("click", closeChat);
  if (chatOverlay) chatOverlay.addEventListener("click", closeChat);

  const chatSend = document.getElementById("chat-send");
  const searchInput = document.getElementById("search-input");
  if (chatSend) chatSend.addEventListener("click", sendChat);
  if (searchInput) searchInput.addEventListener("keydown", handleSearchKey);

  document.querySelectorAll(".lang-switch button").forEach((btn) => {
    btn.addEventListener("click", () => {
      setLang(btn.dataset.lang);
      updateLangButtons();
    });
  });

  updateLangButtons();
});

/* ---------------------------
   LOADERS
--------------------------- */
async function loadServices() {
  const res = await fetch("/api/services");
  services = await res.json();
}

async function loadCategories() {
  const res = await fetch("/api/categories");
  categories = await res.json();
  const el = document.getElementById("category-list");
  if (!el) return;
  el.innerHTML = "";
  categories.forEach((c) => {
    const item = document.createElement("div");
    item.className = "cat-item";
    item.innerHTML = `
      <i data-lucide="${getCategoryIcon(c.name?.en || c.id)}"></i>
      <span>${c.name?.[lang] || c.name?.en || c.id}</span>`;
    item.onclick = () => loadMinistriesInCategory(c);
    el.appendChild(item);
  });
  lucide.createIcons();
}

async function loadMinistriesInCategory(cat) {
  const subList = document.getElementById("sub-list");
  const subTitle = document.getElementById("sub-title");
  if (!subList || !subTitle) return;

  subList.innerHTML = "";
  subTitle.innerText = cat.name?.[lang] || cat.name?.en || cat.id;

  if (cat.ministry_ids && cat.ministry_ids.length) {
    for (let id of cat.ministry_ids) {
      const r = await fetch(`/api/service/${id}`);
      const s = await r.json();
      if (s && s.subservices) {
        s.subservices.forEach((sub) => {
          let li = document.createElement("li");
          li.textContent = sub.name?.[lang] || sub.name?.en || sub.id;
          li.onclick = () => loadQuestions(s, sub);
          subList.appendChild(li);
        });
      }
    }
  } else {
    const svcRes = await fetch("/api/services");
    const all = await svcRes.json();
    all.filter((s) => s.category === cat.id).forEach((s) => {
      s.subservices.forEach((sub) => {
        let li = document.createElement("li");
        li.textContent = sub.name?.[lang] || sub.name?.en || sub.id;
        li.onclick = () => loadQuestions(s, sub);
        subList.appendChild(li);
      });
    });
  }
}

async function loadQuestions(service, sub) {
  currentServiceName = service.name?.[lang] || service.name?.en;
  currentSub = sub;
  const qList = document.getElementById("question-list");
  const qTitle = document.getElementById("q-title");
  if (!qList || !qTitle) return;

  qList.innerHTML = "";
  qTitle.innerText = sub.name?.[lang] || sub.name?.en || sub.id;

  (sub.questions || []).forEach((q) => {
    let li = document.createElement("li");
    li.textContent = q.q?.[lang] || q.q?.en;
    li.onclick = () => showAnswer(service, sub, q);
    qList.appendChild(li);
  });
}

function showAnswer(service, sub, q) {
  const answerBox = document.getElementById("answer-box");
  if (!answerBox) return;

  let html = `<h3>${q.q?.[lang] || q.q?.en}</h3>`;
  html += `<p>${q.answer?.[lang] || q.answer?.en}</p>`;
  answerBox.innerHTML = html;
}

/* ---------------------------
   ADS LOADER
--------------------------- */
async function loadAds() {
  const res = await fetch("/api/ads");
  const ads = await res.json();
  const el = document.getElementById("ads-area");
  if (!el || !ads.length) return;
  el.innerHTML = ads
    .map(
      (a) => `
      <div class="ad-card">
        <i data-lucide="info" class="ad-icon"></i>
        <div>
          <h4>${a.title || "Notice"}</h4>
          <p>${a.body || ""}</p>
        </div>
      </div>`
    )
    .join("");
  lucide.createIcons();
}

/* ---------------------------
   LANGUAGE SWITCH
--------------------------- */
function setLang(l) {
  lang = l;
  localStorage.setItem("portal_lang", l);
  loadCategories();
  if (currentSub) loadQuestions(currentServiceName, currentSub);
}

function updateLangButtons() {
  document.querySelectorAll(".lang-switch button").forEach((btn) => {
    if (!btn) return;
    btn.classList.toggle("active", btn.dataset.lang === lang);
  });
}

/* ---------------------------
   THEME TOGGLE
--------------------------- */
function toggleTheme() {
  const dark = !document.body.classList.contains("dark");
  document.body.classList.toggle("dark", dark);
  localStorage.setItem("portal_theme", dark ? "dark" : "light");
  updateThemeIcon(dark);
}

function updateThemeIcon(isDark) {
  const iconParent = document.getElementById("theme-toggle");
  if (!iconParent) return;
  iconParent.innerHTML = `<i data-lucide="${isDark ? "sun" : "moon"}"></i>`;
  lucide.createIcons();
}

/* ---------------------------
   CHAT FUNCTIONS
--------------------------- */
function openChat() {
  document.getElementById("chat-overlay").classList.add("active");
  document.getElementById("chat-drawer").classList.add("open");
}

function closeChat() {
  document.getElementById("chat-overlay").classList.remove("active");
  document.getElementById("chat-drawer").classList.remove("open");
}

async function sendChat() {
  const input = document.getElementById("chat-text");
  const text = input.value.trim();
  if (!text) return;
  appendChat("user", text);
  input.value = "";

  try {
    const res = await fetch("/api/ai/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: text, top_k: 5 }),
    });
    const data = await res.json();
    appendChat("bot", data.answer || "No answer found.");
  } catch {
    appendChat("bot", "Error contacting AI server.");
  }
}

function appendChat(sender, text) {
  const body = document.getElementById("chat-body");
  if (!body) return;
  const div = document.createElement("div");
  div.className = `chat-msg ${sender === "user" ? "user-msg" : "bot-msg"}`;
  div.innerText = text;
  body.appendChild(div);
  body.scrollTop = body.scrollHeight;
}

/* ---------------------------
   SEARCH HANDLER
--------------------------- */
function handleSearchKey(e) {
  if (e.key === "Enter") {
    const q = e.target.value.trim();
    if (!q) return;
    openChat();
    document.getElementById("chat-text").value = q;
    sendChat();
  }
}

/* ---------------------------
   HELPERS
--------------------------- */
function getCategoryIcon(name) {
  const n = name.toLowerCase();
  if (n.includes("business")) return "briefcase";
  if (n.includes("property")) return "home";
  if (n.includes("health")) return "heart";
  if (n.includes("education")) return "book";
  if (n.includes("transport")) return "car";
  if (n.includes("agriculture")) return "leaf";
  return "grid";
}
