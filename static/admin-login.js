document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const btn = document.getElementById("login-btn");
    const errorMsg = document.getElementById("error-message");
    const originalBtnText = btn.innerHTML;
    
    // Show loading state
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing In...';
    errorMsg.style.display = "none";
    
    try {
        const form = new FormData(e.target);
        const res = await fetch('/admin/login', { 
            method: 'POST', 
            body: form 
        });
        
        if (res.redirected) {
            // Successful login - redirect
            window.location = res.url;
        } else if (res.status === 401) {
            // Invalid credentials
            errorMsg.textContent = "Invalid username or password";
            errorMsg.style.display = "block";
            btn.disabled = false;
            btn.innerHTML = originalBtnText;
        } else {
            // Other error
            errorMsg.textContent = "An error occurred. Please try again.";
            errorMsg.style.display = "block";
            btn.disabled = false;
            btn.innerHTML = originalBtnText;
        }
    } catch (error) {
        console.error("Login error:", error);
        errorMsg.textContent = "Unable to connect to server. Please try again.";
        errorMsg.style.display = "block";
        btn.disabled = false;
        btn.innerHTML = originalBtnText;
    }
});

// Handle Enter key in password field
document.getElementById("password").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        document.getElementById("login-form").requestSubmit();
    }
});