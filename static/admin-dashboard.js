// Global variables
let insightsData = null;

// Initialize dashboard on load
window.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    initializeNavigation();
    initializeMenu();
    initializeTheme();
});

// Navigation between pages
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            
            // Update active nav item
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            // Show corresponding page
            document.querySelectorAll('.page-content').forEach(p => p.classList.remove('active'));
            document.getElementById(`page-${page}`).classList.add('active');
            
            // Load page-specific data
            if (page === 'officers') loadOfficers();
            if (page === 'services') loadServices();
            if (page === 'categories') loadCategories();
            if (page === 'ads') loadAds();
        });
    });
}

// Mobile menu toggle
function initializeMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    menuToggle?.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });
}

// Load dashboard data
async function loadDashboard() {
    try {
        const res = await fetch('/api/admin/insights');
        
        if (res.status === 401) {
            window.location = '/admin/login';
            return;
        }
        
        insightsData = await res.json();
        
        // Update stats
        updateStats(insightsData);
        
        // Create charts
        createAgeChart(insightsData.age_groups);
        createJobsChart(insightsData.jobs);
        createServicesChart(insightsData.services);
        createQuestionsChart(insightsData.questions);
        
        // Load engagements table
        loadEngagements();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        alert('Failed to load dashboard data');
    }
}

// Update stats cards
function updateStats(data) {
    const totalUsers = Object.values(data.age_groups).reduce((a, b) => a + b, 0);
    const activeServices = Object.keys(data.services).length;
    const totalQuestions = Object.keys(data.questions).length;
    const engagements = Object.values(data.services).reduce((a, b) => a + b, 0);
    
    document.getElementById('statTotalUsers').textContent = totalUsers.toLocaleString();
    document.getElementById('statActiveServices').textContent = activeServices;
    document.getElementById('statTotalQuestions').textContent = totalQuestions;
    document.getElementById('statEngagements').textContent = engagements.toLocaleString();
}

// Create age groups chart
function createAgeChart(data) {
    const ctx = document.getElementById('ageChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Users',
                data: Object.values(data),
                backgroundColor: 'rgba(11, 59, 140, 0.7)',
                borderColor: 'rgba(11, 59, 140, 1)',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    borderRadius: 8,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            }
        }
    });
}

// Create jobs distribution chart
function createJobsChart(data) {
    const ctx = document.getElementById('jobChart');
    if (!ctx) return;
    
    const colors = [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 205, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)'
    ];
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    borderRadius: 8
                }
            }
        }
    });
}

// Create services chart
function createServicesChart(data) {
    const ctx = document.getElementById('serviceChart');
    if (!ctx) return;
    
    const colors = [
        'rgba(11, 59, 140, 0.7)',
        'rgba(30, 64, 175, 0.7)',
        'rgba(37, 99, 235, 0.7)',
        'rgba(59, 130, 246, 0.7)',
        'rgba(96, 165, 250, 0.7)'
    ];
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    borderRadius: 8
                }
            }
        }
    });
}

// Create questions chart
function createQuestionsChart(data) {
    const ctx = document.getElementById('questionChart');
    if (!ctx) return;
    
    // Get top 10 questions
    const sorted = Object.entries(data)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    const labels = sorted.map(([q]) => {
        return q.length > 40 ? q.substring(0, 40) + '...' : q;
    });
    const values = sorted.map(([, v]) => v);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: values,
                backgroundColor: 'rgba(5, 150, 105, 0.7)',
                borderColor: 'rgba(5, 150, 105, 1)',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    borderRadius: 8
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });
}

// Load engagements table
async function loadEngagements() {
    try {
        const res = await fetch('/api/admin/engagements');
        const items = await res.json();
        
        const tbody = document.querySelector('#engTable tbody');
        tbody.innerHTML = '';
        
        items.slice(0, 50).forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.age || '-'}</td>
                <td>${item.job || '-'}</td>
                <td>${(item.desires || []).join(', ') || '-'}</td>
                <td>${item.question_clicked || '-'}</td>
                <td>${item.service || '-'}</td>
                <td>${new Date(item.timestamp).toLocaleString()}</td>
            `;
            tbody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading engagements:', error);
    }
}

// Load officers
async function loadOfficers() {
    try {
        const res = await fetch('/api/admin/officers');
        const officers = await res.json();
        
        const tbody = document.querySelector('#officersTable tbody');
        tbody.innerHTML = '';
        
        officers.forEach(officer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${officer.name}</td>
                <td>${officer.role}</td>
                <td>${officer.ministry_id}</td>
                <td>${officer.contact?.email || '-'}</td>
                <td>${officer.contact?.phone || '-'}</td>
                <td>
                    <button class="action-btn edit" onclick="editOfficer('${officer.id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="action-btn delete" onclick="deleteOfficer('${officer.id}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading officers:', error);
    }
}

// Export CSV
document.getElementById('exportCsv')?.addEventListener('click', () => {
    window.location = '/api/admin/export_csv';
});

// Rebuild AI Index
document.getElementById('rebuildIndexBtn')?.addEventListener('click', async () => {
    const btn = document.getElementById('rebuildIndexBtn');
    const status = document.getElementById('rebuildStatus');
    const originalHtml = btn.innerHTML;
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Rebuilding...</span>';
    
    try {
        const res = await fetch('/api/admin/build_index', { method: 'POST' });
        const data = await res.json();
        
        status.className = 'rebuild-status success';
        status.textContent = `Success! Indexed ${data.count} documents. FAISS: ${data.faiss ? 'Enabled' : 'Fallback mode'}`;
        status.style.display = 'block';
        
        setTimeout(() => {
            status.style.display = 'none';
        }, 5000);
        
    } catch (error) {
        console.error('Rebuild error:', error);
        status.className = 'rebuild-status error';
        status.textContent = 'Error: Failed to rebuild index. Check console for details.';
        status.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
    }
});

// Logout
document.getElementById('logoutBtn')?.addEventListener('click', async () => {
    try {
        await fetch('/api/admin/logout', { method: 'POST' });
        window.location = '/admin/login';
    } catch (error) {
        console.error('Logout error:', error);
        window.location = '/admin/login';
    }
});

// Placeholder functions for officer management
function editOfficer(id) {
    alert(`Edit officer: ${id} (Feature coming soon)`);
}

function deleteOfficer(id) {
    if (confirm('Are you sure you want to delete this officer?')) {
        fetch(`/api/admin/officers?id=${id}`, { method: 'DELETE' })
            .then(() => {
                alert('Officer deleted');
                loadOfficers();
            })
            .catch(err => alert('Error deleting officer'));
    }
}

// Load services
async function loadServices() {
    try {
        const res = await fetch('/api/admin/services');
        const services = await res.json();
        
        const tbody = document.querySelector('#servicesTable tbody');
        tbody.innerHTML = '';
        
        services.forEach(service => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${service.id}</td>
                <td>${service.name?.en || service.name}</td>
                <td>${service.category || '-'}</td>
                <td>${service.subservices?.length || 0}</td>
                <td>
                    <button class="action-btn edit" onclick="editService('${service.id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="action-btn delete" onclick="deleteService('${service.id}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

function editService(id) {
    alert(`Edit service: ${id} (Feature coming soon)`);
}

function deleteService(id) {
    if (confirm('Are you sure you want to delete this service?')) {
        fetch(`/api/admin/services/${id}`, { method: 'DELETE' })
            .then(() => {
                alert('Service deleted');
                loadServices();
            })
            .catch(err => alert('Error deleting service'));
    }
}

// Load categories
async function loadCategories() {
    try {
        const res = await fetch('/api/admin/categories');
        const categories = await res.json();
        
        const tbody = document.querySelector('#categoriesTable tbody');
        tbody.innerHTML = '';
        
        categories.forEach(cat => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${cat.id}</td>
                <td>${cat.name?.en || '-'}</td>
                <td>${cat.name?.si || '-'}</td>
                <td>${cat.name?.ta || '-'}</td>
                <td>${cat.ministry_ids?.length || 0} ministries</td>
                <td>
                    <button class="action-btn edit" onclick="editCategory('${cat.id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="action-btn delete" onclick="deleteCategory('${cat.id}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

function editCategory(id) {
    alert(`Edit category: ${id} (Feature coming soon)`);
}

function deleteCategory(id) {
    if (confirm('Are you sure you want to delete this category?')) {
        fetch(`/api/admin/categories?id=${id}`, { method: 'DELETE' })
            .then(() => {
                alert('Category deleted');
                loadCategories();
            })
            .catch(err => alert('Error deleting category'));
    }
}

// Load ads/announcements
async function loadAds() {
    try {
        const res = await fetch('/api/admin/ads');
        const ads = await res.json();
        
        const grid = document.querySelector('.ads-grid');
        grid.innerHTML = '';
        
        ads.forEach(ad => {
            const card = document.createElement('div');
            card.className = 'ad-card-item';
            card.innerHTML = `
                <div class="ad-card-image">
                    <i class="fas fa-bullhorn"></i>
                </div>
                <h3 class="ad-card-title">${ad.title}</h3>
                <p class="ad-card-body">${ad.body || 'No description'}</p>
                ${ad.link ? `<a href="${ad.link}" class="ad-card-link" target="_blank">
                    View Link <i class="fas fa-external-link-alt"></i>
                </a>` : ''}
                <div class="ad-card-actions">
                    <button class="action-btn edit" onclick="editAd('${ad.id}')">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="action-btn delete" onclick="deleteAd('${ad.id}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            `;
            grid.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error loading ads:', error);
    }
}

function editAd(id) {
    alert(`Edit announcement: ${id} (Feature coming soon)`);
}

function deleteAd(id) {
    if (confirm('Are you sure you want to delete this announcement?')) {
        fetch(`/api/admin/ads?id=${id}`, { method: 'DELETE' })
            .then(() => {
                alert('Announcement deleted');
                loadAds();
            })
            .catch(err => alert('Error deleting announcement'));
    }
}

// Theme toggle
function initializeTheme() {
    const themeBtns = document.querySelectorAll('.theme-btn-header');
    const savedTheme = localStorage.getItem('admin-theme') || 'dark'; // Default to dark
    
    // Apply saved theme
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeBtns.forEach(btn => {
        if (btn.dataset.theme === savedTheme) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Theme button click handlers
    themeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const theme = btn.dataset.theme;
            
            // Update active button
            themeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Apply theme
            document.documentElement.setAttribute('data-theme', theme);
            
            // Save preference
            localStorage.setItem('admin-theme', theme);
        });
    });
}