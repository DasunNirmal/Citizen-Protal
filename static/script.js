// let lang = "en";
// let services = [];
// let currentServiceName = "";

// async function loadServices() {
//     const res = await fetch("/api/services");
//     services = await res.json();
//     const list = document.getElementById("service-list");
//     list.innerHTML = "";
    
//     services.forEach(s => {
//         let li = document.createElement("li");
//         li.textContent = s.name[lang] || s.name.en;
//         li.onclick = () => loadSubservices(s);
//         list.appendChild(li);
//     });
// }

// function setLang(l) {
//     lang = l;
//     loadServices();
//     document.getElementById("sub-list").innerHTML = "";
//     document.getElementById("question-list").innerHTML = "";
//     document.getElementById("answer-box").innerHTML = "";
//     document.getElementById("sub-title").innerText = "Select Subservice";
//     document.getElementById("q-title").innerText = "Select Question";
// }

// function loadSubservices(service) {
//     currentServiceName = service.name[lang] || service.name.en;
//     const subList = document.getElementById("sub-list");
//     subList.innerHTML = "";
//     document.getElementById("sub-title").innerText = currentServiceName;
//     document.getElementById("question-list").innerHTML = "";
//     document.getElementById("answer-box").innerHTML = "";
//     document.getElementById("q-title").innerText = "Select Question";
    
//     (service.subservices || []).forEach(sub => {
//         let li = document.createElement("li");
//         li.textContent = sub.name[lang] || sub.name.en;
//         li.onclick = () => loadQuestions(sub);
//         subList.appendChild(li);
//     });
// }

// function loadQuestions(sub) {
//     const qList = document.getElementById("question-list");
//     qList.innerHTML = "";
//     document.getElementById("q-title").innerText = sub.name[lang] || sub.name.en;
//     document.getElementById("answer-box").innerHTML = "";
    
//     (sub.questions || []).forEach(q => {
//         let li = document.createElement("li");
//         li.textContent = q.q[lang] || q.q.en;
//         li.onclick = () => showAnswer(q);
//         qList.appendChild(li);
//     });
// }

// function showAnswer(q) {
//     let html = `<h3>${q.q[lang] || q.q.en}</h3>`;
//     html += `<p>${q.answer[lang] || q.answer.en}</p>`;
    
//     if (q.downloads && q.downloads.length) {
//         html += `<p><b>Downloads:</b> ${q.downloads.map(d=>`<a href="${d}" target="_blank">${d.split("/").pop()}</a>`).join(", ")}</p>`;
//     }
    
//     if (q.location) {
//         html += `<p><b>Location:</b> <a href="${q.location}" target="_blank">View Map</a></p>`;
//     }
    
//     if (q.instructions) {
//         html += `<p><b>Instructions:</b> ${q.instructions}</p>`;
//     }
    
//     document.getElementById("answer-box").innerHTML = html;
    
//     // Prompt for optional demographics (non-blocking modal could be used)
//     setTimeout(async () => {
//         let age = prompt("Enter your age (optional):");
//         let job = prompt("Enter your job (optional):");
//         let desire = prompt("What is your main interest here (optional)?");
        
//         await fetch("/api/engagement", {
//             method: "POST",
//             headers:{ "Content-Type":"application/json" },
//             body: JSON.stringify({
//                 user_id: null,
//                 age: age,
//                 job: job,
//                 desires: desire ? [desire] : [],
//                 question_clicked: q.q[lang] || q.q.en,
//                 service: currentServiceName
//             })
//         });
//     }, 200);
// }

// window.onload = loadServices;

let lang = "en";
let services = [];
let categories = [];
let currentServiceName = "";
let currentSub = null;
let profile_id = null;

// load categories
async function loadCategories(){
    const res = await fetch("/api/categories");
    categories = await res.json();
    const el = document.getElementById("category-list");
    el.innerHTML = "";
    categories.forEach(c=>{
        const btn = document.createElement("div");
        btn.className = "cat-item";
        btn.textContent = c.name?.[lang] || c.name?.en || c.id;
        btn.onclick = ()=> loadMinistriesInCategory(c);
        el.appendChild(btn);
});
// load ads
loadAds();
}

async function loadMinistriesInCategory(cat){
    document.getElementById("sub-list").innerHTML = "";
    document.getElementById("sub-title").innerText = cat.name?.[lang] ||
cat.name?.en || cat.id;
    // If categories document contains ministry_ids show them, else fetch services to filter
    if(cat.ministry_ids && cat.ministry_ids.length){
        // fetch each ministry by id
        for(let id of cat.ministry_ids){
            const r = await fetch(`/api/service/${id}`);
            const s = await r.json();
                if(s && s.subservices){
                    s.subservices.forEach(sub=>{
                    let li = document.createElement("li");
                    li.textContent = sub.name?.[lang] || sub.name?.en || sub.id;
                    li.onclick = ()=> loadQuestions(s, sub);
                    document.getElementById("sub-list").appendChild(li);
                });
            }   
        }
    } else {
        // fallback: query services and filter by c.id in their category field
        const svcRes = await fetch("/api/services");
        const all = await svcRes.json();
        all.filter(s=>s.category===cat.id).forEach(s=> {
        s.subservices.forEach(sub=> {
            let li = document.createElement("li");
            li.textContent = sub.name?.[lang] || sub.name?.en || sub.id;
            li.onclick = ()=> loadQuestions(s, sub);
            document.getElementById("sub-list").appendChild(li);
            });
        });
    }
}

async function loadQuestions(service, sub){
    currentServiceName = service.name?.[lang] || service.name?.en;
    currentSub = sub;
    const qList = document.getElementById("question-list");
    qList.innerHTML = "";
    document.getElementById("q-title").innerText = sub.name?.[lang] ||
sub.name?.en || sub.id;
    (sub.questions || []).forEach(q=>{
        let li = document.createElement("li");
        li.textContent = q.q?.[lang] || q.q?.en;
        li.onclick = ()=> showAnswer(service, sub, q);
        qList.appendChild(li);
    });
}

function showAnswer(service, sub, q){
    let html = `<h3>${q.q?.[lang] || q.q?.en}</h3>`;
    html += `<p>${q.answer?.[lang] || q.answer?.en}</p>`;
    if(q.downloads && q.downloads.length){
        html += `<p><b>Downloads:</b> ${q.downloads.map(d=>`<a href="${d}"
        target="_blank">${d.split("/").pop()}</a>`).join(", ")}</p>`;
    }
    if(q.location){
        html += `<p><b>Location:</b> <a href="${q.location}" target="_blank">View
        Map</a></p>`;
    }
    if(q.instructions){
        html += `<p><b>Instructions:</b> ${q.instructions}</p>`;
    }
    document.getElementById("answer-box").innerHTML = html;
    // log engagement non-blocking (without prompts)
    fetch("/api/engagement", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({
        user_id: profile_id, age:null, job:null, desires: [], question_clicked:
        q.q?.[lang] || q.q?.en, service: currentServiceName
        })
    });
}

// Chat UI
function openChat(){ document.getElementById("chat-panel").style.display =
"block"; }
function closeChat(){ document.getElementById("chat-panel").style.display =
"none"; }