document.getElementById("login-form").onsubmit = async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const res = await fetch('/admin/login', { method:'POST', body: form });
    if (res.redirected) window.location = res.url;
    else {
        // Try to fetch insights to check if logged in
        loadDashboard();
    }
};

async function loadDashboard(){
    const dashEl = document.getElementById("dashboard");
    try {
        const r = await fetch('/api/admin/insights');
        if (r.status === 401) {
            document.getElementById("login-box").style.display = "block";
            dashEl.style.display = "none";
            return;
        }
        const data = await r.json();
        document.getElementById("login-box").style.display = "none";
        dashEl.style.display = "block";

        // Age Chart
        new Chart(document.getElementById("ageChart"), { 
            type:'bar',
            data:{ 
                labels:Object.keys(data.age_groups),
                datasets:[{
                    label:"Users by Age",
                    data:Object.values(data.age_groups),
                    backgroundColor:'rgba(11, 59, 140, 0.6)',
                    borderColor:'rgba(11, 59, 140, 1)',
                    borderWidth:1
                }] 
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'User Age Groups'
                    }
                }
            }
        });

        // Jobs Chart
        new Chart(document.getElementById("jobChart"), { 
            type:'pie',
            data:{ 
                labels:Object.keys(data.jobs), 
                datasets:[{
                    label:"Jobs",
                    data:Object.values(data.jobs),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ]
                }] 
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'User Jobs Distribution'
                    }
                }
            }
        });

        // Services Chart
        new Chart(document.getElementById("serviceChart"), { 
            type:'doughnut',
            data:{ 
                labels:Object.keys(data.services), 
                datasets:[{
                    label:"Services",
                    data:Object.values(data.services),
                    backgroundColor: [
                        'rgba(11, 59, 140, 0.6)',
                        'rgba(30, 64, 175, 0.6)',
                        'rgba(37, 99, 235, 0.6)',
                        'rgba(59, 130, 246, 0.6)',
                        'rgba(96, 165, 250, 0.6)'
                    ]
                }] 
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Popular Services'
                    }
                }
            }
        });

        // Questions Chart
        new Chart(document.getElementById("questionChart"), { 
            type:'bar',
            data:{ 
                labels:Object.keys(data.questions).slice(0,10),
                datasets:[{
                    label:"Top Questions",
                    data:Object.values(data.questions).slice(0,10),
                    backgroundColor:'rgba(5, 150, 105, 0.6)',
                    borderColor:'rgba(5, 150, 105, 1)',
                    borderWidth:1
                }] 
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Most Asked Questions'
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            maxRotation: 45
                        }
                    }
                }
            }
        });

        // Premium suggestions list
        const pl = document.getElementById("premiumList");
        pl.innerHTML = data.premium_suggestions.length ? 
            data.premium_suggestions.map(p => `<div>User: ${p.user} | Question: ${p.question} | Count: ${p.count}</div>`).join("") : 
            "<div>No premium suggestions yet</div>";

        // Load engagements table
        const res = await fetch('/api/admin/engagements');
        const items = await res.json();
        const tbody = document.querySelector("#engTable tbody");
        tbody.innerHTML = "";
        items.forEach(it=>{
            const row = `<tr>
                <td>${it.age||""}</td>
                <td>${it.job||""}</td>
                <td>${(it.desires||[]).join(", ")}</td>
                <td>${it.question_clicked||""}</td>
                <td>${it.service||""}</td>
                <td>${it.timestamp||""}</td>
            </tr>`;
            tbody.insertAdjacentHTML('beforeend', row);
        });

    } catch (err) {
        console.error(err);
        alert("Error loading dashboard data");
    }
}

document.getElementById("logoutBtn")?.addEventListener('click', async ()=>{
    await fetch('/api/admin/logout', {method:'POST'});
    window.location="/admin";
});

document.getElementById("exportCsv")?.addEventListener('click', ()=>{
    window.location = '/api/admin/export_csv'; 
});

window.onload = loadDashboard;