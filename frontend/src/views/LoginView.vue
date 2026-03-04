<template>
  <div class="login-page">
    <div class="login-container fade-in">
      <div class="brand-section">
        <h2>Welcome Back</h2>
        <p>Sign in to access your portal.</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label>Email</label>
          <div class="input-wrapper">
            <input
              v-model="email"
              type="email"
              placeholder="Enter your email"
              required
            />
          </div>
        </div>

        <div class="input-group">
          <label>Password</label>
          <div class="input-wrapper">
            <input
              v-model="password"
              type="password"
              placeholder="Enter your password"
              required
            />
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          <span v-if="isLoading" class="spinner"></span>
          <span v-else>Login</span>
        </button>
      </form>

      <p class="register-link">
        Don't have an account?
        <router-link to="/register">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { login } from "../api/auth"

export default {
  data() {
    return {
      email: "",
      password: "",
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      try {
        const response = await login({
          email: this.email,
          password: this.password
        });
        
        const data = response.data;
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("role", data.role);
        
        if (data.role === "admin") {
          this.$router.push("/admin");
        } else if (data.role === "company") {
          this.$router.push("/company");
        } else if (data.role === "student") {
          this.$router.push("/student");
        }
      } catch (error) {
        alert("Invalid login credentials");
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>


.login-page {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f7f6;
  padding: 2rem;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  box-sizing: border-box;
  margin: 0;
}


.login-container {
  background: #ffffff;
  border-radius: 12px;
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: #333;
}


.brand-section {
  text-align: center;
  margin-bottom: 2rem;
}

.brand-section h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.brand-section p {
  color: #666;
  font-size: 0.95rem;
  margin: 0;
}


.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
}

.input-wrapper {
  position: relative;
}

input {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  border: 1px solid #cbd5e0;
  background: #fff;
  color: #2d3748;
  font-size: 1rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

input::placeholder {
  color: #a0aec0;
}

input:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

/* Button */
.submit-btn {
  margin-top: 0.5rem;
  width: 100%;
  padding: 0.8rem;
  border-radius: 8px;
  border: none;
  background: #3182ce;
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.submit-btn:hover:not(:disabled) {
  background: #2b6cb0;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}


.register-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #718096;
}

.register-link a {
  color: #3182ce;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.4rem;
}

.register-link a:hover {
  text-decoration: underline;
}


.fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}


@media (max-width: 480px) {
  .login-container {
    padding: 1.5rem;
  }
}
</style>