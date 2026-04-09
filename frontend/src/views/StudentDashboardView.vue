<template>
  <div class="dashboard-page">
    <header class="dashboard-header">
      <div class="header-content">
        <h2>Student Dashboard</h2>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </header>

    <main class="dashboard-main fade-in">
      <nav class="dashboard-nav">
        <button @click="activeTab = 'profile'" :class="['nav-btn', { active: activeTab === 'profile' }]">My Profile</button>
        <button @click="activeTab = 'jobs'" :class="['nav-btn', { active: activeTab === 'jobs' }]">Available Jobs</button>
        <button @click="activeTab = 'applications'" :class="['nav-btn', { active: activeTab === 'applications' }]">My Applications</button>
        <button @click="activeTab = 'placements'" :class="['nav-btn', { active: activeTab === 'placements' }]">Placement History</button>
      </nav>

      <section v-if="activeTab === 'profile'" class="dashboard-section">
        <h3>My Profile</h3>
        <div v-if="profileLoading" class="loading-state">Loading profile...</div>
        <div v-else class="card form-card">
          <form @submit.prevent="handleUpdateProfile" class="profile-form">
            <div class="row-group">
              <div class="input-group">
                <label>Full Name</label>
                <input v-model="profile.name" type="text" required />
              </div>
              <div class="input-group">
                <label>Branch</label>
                <select v-model="profile.branch_id" required>
                  <option v-for="branch in branches" :key="branch.id" :value="branch.id">{{ branch.name }}</option>
                </select>
              </div>
            </div>
            <div class="row-group">
              <div class="input-group">
                <label>CGPA</label>
                <input v-model="profile.cgpa" type="number" step="0.01" min="0" max="10" />
              </div>
              <div class="input-group">
                <label>Graduation Year</label>
                <input v-model="profile.graduation_year" type="number" min="2000" max="2100" />
              </div>
            </div>
            <div class="row-group">
              <div class="input-group">
                <label>Skills</label>
                <textarea v-model="profile.skills" rows="3" placeholder="E.g., Python, Vue, Database Management"></textarea>
              </div>
              <div class="input-group">
                <label>Experience</label>
                <textarea v-model="profile.experience" rows="3" placeholder="Previous internships, jobs, etc."></textarea>
              </div>
            </div>
            <div class="input-group full-width">
              <label>Resume Link</label>
              <input v-model="profile.resume_link" type="url" placeholder="https://link-to-your-resume.com" />
            </div>
            <div class="form-actions">
              <button type="submit" class="submit-btn" :disabled="isUpdatingProfile">
                <span v-if="isUpdatingProfile" class="spinner"></span>
                <span v-else>Update Profile</span>
              </button>
            </div>
          </form>
        </div>
      </section>

      <section v-if="activeTab === 'jobs'" class="dashboard-section">
        <div class="section-header-horizontal" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <h3 style="margin: 0;">Available Jobs</h3>
          <div class="search-bar" style="width: 100%; max-width: 300px;">
            <input v-model="searchQuery" type="text" placeholder="Search by title, company, or skills..." class="search-input" style="width: 100%; padding: 0.6rem; border: 1px solid #cbd5e0; border-radius: 6px;" />
          </div>
        </div>
        <div v-if="jobsLoading" class="loading-state">Loading jobs...</div>
        <div v-else-if="filteredJobs.length === 0" class="empty-state">No jobs match your search criteria or none available.</div>
        <div v-else class="card-list">
          <div v-for="job in filteredJobs" :key="job.id" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ job.company }}</h4>
              <span class="job-title">{{ job.title }}</span>
            </div>
            <div class="card-body">
              <p class="description">{{ job.description }}</p>
              <div class="job-details">
                <span><strong>Job ID:</strong> {{ job.id }}</span>
                <span><strong>Min CGPA:</strong> {{ job.min_cgpa }}</span>
                <span><strong>Salary:</strong> {{ job.salary }}</span>
                <span><strong>Deadline:</strong> {{ formatDate(job.deadline) }}</span>
                <span><strong>Eligible Branches:</strong> {{ job.eligible_branches?.join(', ') || 'All' }}</span>
              </div>
            </div>
            <div class="card-footer">
              <button v-if="hasApplied(job.id)" class="apply-btn applied" disabled>
                Already Applied
              </button>
              <button v-else
                @click="handleApply(job.id)" 
                class="apply-btn"
                :disabled="applyingId === job.id"
              >
                <span v-if="applyingId === job.id" class="spinner"></span>
                <span v-else>Apply</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <section v-if="activeTab === 'applications'" class="dashboard-section">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>My Applications</h3>
            <button @click="triggerCSVExport" :disabled="exportingCSV" class="action-btn" style="background-color: #2c3e50; color: white;">
                <span v-if="exportingCSV">Processing...</span>
                <span v-else>Export to CSV</span>
            </button>
        </div>
        <div v-if="historyLoading" class="loading-state">Loading applications...</div>
        <div v-else-if="applications.length === 0" class="empty-state">You haven't applied to any jobs yet.</div>
        <div v-else class="card-list">
          <div v-for="app in applications" :key="app.application_id" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ app.company }}</h4>
              <span :class="['status-badge', app.status?.toLowerCase() || 'applied']">{{ app.status || 'applied' }}</span>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>Application ID:</strong> {{ app.application_id }}</span>
                <span><strong>Job ID:</strong> {{ app.job_id }}</span>
                <span><strong>Job Title:</strong> {{ app.job_title }}</span>
                <span><strong>Offered Salary:</strong> {{ app.offered_salary }}</span>
                <span><strong>Applied On:</strong> {{ formatDate(app.applied_at) }}</span>
                <span v-if="app.interview_date"><strong>Interview Date:</strong> {{ formatDate(app.interview_date) }}</span>
                <span v-if="app.feedback"><strong>Feedback:</strong> {{ app.feedback }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section v-if="activeTab === 'placements'" class="dashboard-section">
        <h3>Placement History</h3>
        <div v-if="placementsLoading" class="loading-state">Loading placements...</div>
        <div v-else-if="placements.length === 0" class="empty-state">No placements yet.</div>
        <div v-else class="card-list">
          <div v-for="(p, index) in placements" :key="index" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ p.company }}</h4>
              <span class="job-title">{{ p.job_title }}</span>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>Offered Salary:</strong> {{ p.offered_salary }}</span>
                <span><strong>Joining Date:</strong> {{ formatDate(p.joining_date) }}</span>
              </div>
            </div>
            <div class="card-footer" style="padding: 10px 15px; border-top: 1px solid #e1e8ed; text-align: right;">
              <button @click="downloadOfferLetter(p)" class="action-btn" style="background-color: #28a745; color: white; padding: 6px 12px; border: none; border-radius: 4px; cursor: pointer;">
                Download Offer Letter
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { fetchJobs, applyJob, fetchApplications, fetchPlacements, fetchProfile, updateProfile, exportCSV } from '../api/student';
import { logoutAPI, getBranches } from '../api/auth';

export default {
  data() {
    return {
      activeTab: 'jobs',
      profile: {
        name: '',
        branch_id: '',
        cgpa: '',
        graduation_year: '',
        skills: '',
        experience: '',
        resume_link: ''
      },
      branches: [],
      jobs: [],
      searchQuery: '',
      applications: [],
      placements: [],
      profileLoading: true,
      isUpdatingProfile: false,
      jobsLoading: true,
      historyLoading: true,
      placementsLoading: true,
      applyingId: null,
      exportingCSV: false
    };
  },
  async created() {
    await Promise.all([
      this.loadProfile(),
      this.loadBranches(),
      this.loadJobs(), 
      this.loadApplications(), 
      this.loadPlacements()
    ]);
  },
  computed: {
    filteredJobs() {
      if (!this.searchQuery) return this.jobs;
      const lowerQuery = this.searchQuery.toLowerCase();
      return this.jobs.filter(job => {
        return (
          (job.title && job.title.toLowerCase().includes(lowerQuery)) ||
          (job.company && job.company.toLowerCase().includes(lowerQuery)) ||
          (job.description && job.description.toLowerCase().includes(lowerQuery))
        );
      });
    }
  },
  methods: {
    async loadProfile() {
      this.profileLoading = true;
      try {
        const res = await fetchProfile();
        this.profile = res.data;
      } catch (err) {
        console.error("Failed to load profile:", err);
      } finally {
        this.profileLoading = false;
      }
    },
    async loadBranches() {
      try {
        const res = await getBranches();
        this.branches = res.data;
      } catch (err) {
        console.error("Failed to load branches:", err);
      }
    },
    async handleUpdateProfile() {
      this.isUpdatingProfile = true;
      try {
        await updateProfile(this.profile);
        alert("Profile updated successfully!");
        this.loadProfile();
      } catch (err) {
        alert("Failed to update profile: " + (err.response?.data?.message || err.message));
      } finally {
        this.isUpdatingProfile = false;
      }
    },
    async triggerCSVExport() {
      this.exportingCSV = true;
      try {
        const res = await exportCSV();
        alert(res.data.message || "Export started. You'll receive an email shortly.");
      } catch (err) {
        alert("Failed to start export: " + (err.response?.data?.message || err.message));
      } finally {
        this.exportingCSV = false;
      }
    },
    hasApplied(jobId) {
      return this.applications.some(app => app.job_id === jobId);
    },
    async loadJobs() {
      this.jobsLoading = true;
      try {
        const res = await fetchJobs();
        if (Array.isArray(res.data)) {
          this.jobs = res.data;
        } else {
          this.jobs = [];
        }
      } catch (err) {
        console.error("Failed to fetch jobs:", err);
      } finally {
        this.jobsLoading = false;
      }
    },
    async loadApplications() {
      this.historyLoading = true;
      try {
        const res = await fetchApplications();
        if (Array.isArray(res.data)) {
          this.applications = res.data;
        } else {
          this.applications = [];
        }
      } catch (err) {
        console.error("Failed to fetch applications:", err);
      } finally {
        this.historyLoading = false;
      }
    },
    async loadPlacements() {
      this.placementsLoading = true;
      try {
        const res = await fetchPlacements();
        if (Array.isArray(res.data)) {
          this.placements = res.data;
        } else {
          this.placements = [];
        }
      } catch (err) {
        console.error("Failed to fetch placements:", err);
      } finally {
        this.placementsLoading = false;
      }
    },
    downloadOfferLetter(placement) {
      const text = `OFFICIAL PLACEMENT CONFIRMATION\n\nCompany: ${placement.company}\nTitle: ${placement.job_title}\nOffered Salary: ${placement.offered_salary}\nJoining Date: ${placement.joining_date}\n\nCongratulations on your selection!`;
      const blob = new Blob([text], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Offer_Letter_${placement.company}.txt`;
      a.click();
      window.URL.revokeObjectURL(url);
    },
    async handleApply(jobId) {
      if (!confirm("Are you sure you want to apply for this job?")) return;
      this.applyingId = jobId;
      try {
        const res = await applyJob(jobId);
        alert(res.data.message || "Application submitted successfully");
        await this.loadApplications();
      } catch (err) {
        const message = err.response?.data?.message || "Failed to apply";
        alert(`Error: ${message}`);
      } finally {
        this.applyingId = null;
      }
    },
    async handleLogout() {
      try {
        await logoutAPI();
      } catch (err) {
        console.error("Backend logout failed:", err);
      } finally {
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        this.$router.push("/");
      }
    },
    formatDate(dateString) {
      if (!dateString) return "N/A";
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    }
  }
};
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  width: 100vw;
  background: #f4f7f6;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #333;
  margin: 0;
  box-sizing: border-box;
}

.dashboard-header {
  background: #ffffff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.dashboard-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 1rem;
  overflow-x: auto;
}

.nav-btn {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: #718096;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-btn:hover {
  background: #edf2f7;
  color: #2d3748;
}

.nav-btn.active {
  background: #ebf8ff;
  color: #3182ce;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.row-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.input-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
}

.input-group input, .input-group select, .input-group textarea {
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

.input-group input:focus, .input-group select:focus, .input-group textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

.form-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

.submit-btn {
  padding: 0.6rem 2rem;
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

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
  font-weight: 700;
}

.logout-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: #4a5568;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #f7fafc;
  color: #2d3748;
  border-color: #cbd5e0;
}

.dashboard-main {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.dashboard-section h3 {
  font-size: 1.25rem;
  color: #2d3748;
  margin: 0 0 1rem 0;
  font-weight: 600;
}

.card-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.card {
  background: #ffffff;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #edf2f7;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.company-name {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
}

.job-title {
  font-size: 0.95rem;
  color: #4a5568;
  font-weight: 500;
  display: block;
  margin-top: 0.25rem;
}

.card-body .description {
  font-size: 0.9rem;
  color: #718096;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.job-details {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.85rem;
  color: #4a5568;
}

.job-details strong {
  color: #2d3748;
}

.card-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #edf2f7;
}

.apply-btn {
  width: 100%;
  padding: 0.6rem;
  border-radius: 6px;
  border: none;
  background: #3182ce;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.apply-btn:hover:not(:disabled) {
  background: #2b6cb0;
}

.apply-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.apply-btn.applied {
  background: #e2e8f0;
  color: #4a5568;
  opacity: 1;
}

.status-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.pending, .status-badge.applied {
  background: #feebc8;
  color: #dd6b20;
}

.status-badge.shortlisted {
  background: #ebf8ff;
  color: #3182ce;
}

.status-badge.interview_scheduled {
  background: #e9d8fd;
  color: #6b46c1;
}

.status-badge.selected, .status-badge.approved {
  background: #c6f6d5;
  color: #38a169;
}

.status-badge.rejected {
  background: #fed7d7;
  color: #e53e3e;
}

.status-badge.closed {
  background: #e2e8f0;
  color: #4a5568;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #718096;
  background: #ffffff;
  border-radius: 8px;
  border: 1px dashed #cbd5e0;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
  .dashboard-main {
    padding: 0 1rem;
  }
  .card-list {
    grid-template-columns: 1fr;
  }
}
</style>
