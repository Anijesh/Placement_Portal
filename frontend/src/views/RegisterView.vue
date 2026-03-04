<template>
  <div class="register-page">
    <div class="register-container fade-in">
      <div class="brand-section">
        <h2>Join Us Today</h2>
        <p>Create an account to start your journey.</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="input-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="Enter your email" required />
        </div>

        <div class="input-group">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="Create a password" required />
        </div>

        <div class="input-group">
          <label>Register As</label>
          <select v-model="form.role">
            <option value="student">Student</option>
            <option value="company">Company</option>
          </select>
        </div>

        <!-- Student Fields -->
        <div v-if="form.role === 'student'" class="dynamic-fields slide-down">
          <div class="input-group">
            <label>Name</label>
            <input v-model="form.name" type="text" placeholder="Enter your full name" required />
          </div>
          <div class="input-group">
            <label>Branch</label>
            <select v-model="form.branch_id" required>
              <option value="" disabled>Select your branch</option>
              <option v-for="branch in branches" :key="branch.id" :value="branch.id">
                {{ branch.name }}
              </option>
            </select>
          </div>
          
          <div class="row-group">
            <div class="input-group">
              <label>CGPA</label>
              <input v-model="form.cgpa" type="number" step="0.01" min="0" max="10" placeholder="e.g. 8.5" required />
            </div>
            
            <div class="input-group">
              <label>Graduation Year</label>
              <input v-model="form.graduation_year" type="number" min="2000" max="2100" placeholder="e.g. 2024" required />
            </div>
          </div>

          <div class="input-group">
            <label>Skills</label>
            <textarea v-model="form.skills" placeholder="List your skills (comma separated)" rows="2"></textarea>
          </div>
        </div>

        <!-- Company Fields -->
        <div v-if="form.role === 'company'" class="dynamic-fields slide-down">
          <div class="input-group">
            <label>Company Name</label>
            <input v-model="form.name" type="text" placeholder="Enter company name" required />
          </div>

          <div class="row-group">
            <div class="input-group">
              <label>Industry</label>
              <input v-model="form.industry" type="text" placeholder="e.g. IT, Finance" required />
            </div>

            <div class="input-group">
              <label>Location</label>
              <input v-model="form.location" type="text" placeholder="City or Country" required />
            </div>
          </div>

          <div class="input-group">
            <label>Website</label>
            <input v-model="form.website" type="url" placeholder="https://example.com" />
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          <span v-if="isLoading" class="spinner"></span>
          <span v-else>Create Account</span>
        </button>
      </form>

      <p class="login-link">
        Already have an account? <router-link to="/">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { register, getBranches } from "../api/auth";

export default {
  data() {
    return {
      isLoading: false,
      branches: [],
      form: {
        email: "",
        password: "",
        role: "student",
        // Student specific
        branch_id: "",
        cgpa: "",
        graduation_year: "",
        skills: "",
        // Company specific
        name: "",
        industry: "",
        location: "",
        website: ""
      }
    };
  },
  async mounted() {
    try {
      const response = await getBranches();
      this.branches = response.data;
    } catch (error) {
      console.error("Failed to load branches", error);
    }
  },
  methods: {
    async handleRegister() {
      this.isLoading = true;
      try {
        const payload = {
          email: this.form.email,
          password: this.form.password,
          role: this.form.role,
        };

        if (this.form.role === 'student') {
          payload.branch_id = this.form.branch_id;
          payload.cgpa = parseFloat(this.form.cgpa);
          payload.graduation_year = parseInt(this.form.graduation_year);
          payload.skills = this.form.skills;
        } else if (this.form.role === 'company') {
          payload.name = this.form.name;
          payload.industry = this.form.industry;
          payload.location = this.form.location;
          payload.website = this.form.website;
        }

        await register(payload);
        alert("Registration successful");
        this.$router.push("/");
      } catch (error) {
        alert(error.response?.data?.message || "Registration failed");
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Base Layout */
.register-page {
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

/* Basic Container */
.register-container {
  background: #ffffff;
  border-radius: 12px;
  padding: 2.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: #333;
  margin: 2rem 0;
}

/* Brand Section */
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

/* Form Styles */
.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.row-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.1rem;
}

label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
}

input, select, textarea {
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

input::placeholder, textarea::placeholder {
  color: #a0aec0;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

select option {
  color: #333;
}

textarea {
  resize: vertical;
  min-height: 80px;
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

/* Login Link */
.login-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #718096;
}

.login-link a {
  color: #3182ce;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.4rem;
}

.login-link a:hover {
  text-decoration: underline;
}

/* Animations */
.fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.slide-down {
  animation: slideDown 0.3s ease-out forwards;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
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

/* Responsive */
@media (max-width: 480px) {
  .register-container {
    padding: 1.5rem;
  }
  .row-group {
    grid-template-columns: 1fr;
  }
}
</style>