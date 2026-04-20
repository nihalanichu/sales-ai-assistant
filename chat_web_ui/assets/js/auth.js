// ===============================
// auth.js
// Handles Login & Signup logic
// ===============================

import { loginUser, signupUser } from "../api/authApi.js";
import { setToken } from "../utils/storage.js";

// -------------------------------
// LOGIN FUNCTION
// -------------------------------
export function initLogin() {
const loginBtn = document.getElementById("loginBtn");

if (!loginBtn) return;

loginBtn.addEventListener("click", async () => {
const email = document.getElementById("email").value.trim();
const password = document.getElementById("password").value.trim();

```
if (!email || !password) {
  showError("Please fill all fields");
  return;
}

try {
  const res = await loginUser({ email, password });

  if (res.ok) {
    const data = await res.json();

    // Save token
    setToken(data.access_token || data.token);

    // Redirect to chat
    window.location.href = "/pages/chat.html";
  } else {
    const err = await res.json();
    showError(err.message || "Invalid credentials");
  }
} catch (error) {
  showError("Server error. Try again.");
}
```

});
}

// -------------------------------
// SIGNUP FUNCTION
// -------------------------------
export function initSignup() {
const signupBtn = document.getElementById("signupBtn");

if (!signupBtn) return;

signupBtn.addEventListener("click", async () => {
const full_name = document.getElementById("full_name").value.trim();
const email = document.getElementById("email").value.trim();
const password = document.getElementById("password").value.trim();

```
if (!full_name || !email || !password) {
  showError("All fields are required");
  return;
}

try {
  const res = await signupUser({ full_name, email, password });

  if (res.ok) {
    alert("Signup successful! Please login.");
    window.location.href = "/pages/login.html";
  } else {
    const err = await res.json();
    showError(err.message || "Signup failed");
  }
} catch (error) {
  showError("Server error. Try again.");
}
```

});
}

// -------------------------------
// ERROR HANDLER
// -------------------------------
function showError(message) {
const errorEl = document.getElementById("errorMsg");
if (!errorEl) return;

errorEl.innerText = message;
errorEl.classList.remove("d-none");
}
