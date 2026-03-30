<template>
  <div class="dashboard-page">
    <header class="dashboard-header">
      <div class="header-content">
        <h2>Student Dashboard</h2>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </header>

    <main class="dashboard-main fade-in">
      <section class="dashboard-section">
        <h3>Available Jobs</h3>
        <div v-if="jobsLoading" class="loading-state">Loading jobs...</div>
        <div v-else-if="jobs.length === 0" class="empty-state">No jobs available right now.</div>
        <div v-else class="card-list">
          <div v-for="job in jobs" :key="job.id" class="card">
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

      <section class="dashboard-section">
        <h3>My Applications</h3>
        <div v-if="historyLoading" class="loading-state">Loading applications...</div>
        <div v-else-if="applications.length === 0" class="empty-state">You haven't applied to any jobs yet.</div>
        <div v-else class="card-list">
          <div v-for="app in applications" :key="app.application_id" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ app.company }}</h4>
              <span class="job-title">{{ app.job_title }}</span>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>Application ID:</strong> {{ app.application_id }}</span>
                <span><strong>Job ID:</strong> {{ app.job_id }}</span>
                <span><strong>Offered Salary:</strong> {{ app.offered_salary }}</span>
                <span><strong>Status:</strong> <span :class="['status-badge', app.status.toLowerCase()]">{{ app.status }}</span></span>
                <span><strong>Applied On:</strong> {{ formatDate(app.applied_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="dashboard-section">
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
                <span><strong>Salary:</strong> {{ p.salary }}</span>
                <span><strong>Joining Date:</strong> {{ formatDate(p.joining_date) }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { fetchJobs, applyJob, fetchApplications, fetchPlacements } from '../api/student';
import { logoutAPI } from '../api/auth';

export default {
  data() {
    return {
      jobs: [],
      applications: [],
      placements: [],
      jobsLoading: true,
      historyLoading: true,
      placementsLoading: true,
      applyingId: null
    };
  },
  async created() {
    await Promise.all([this.loadJobs(), this.loadApplications(), this.loadPlacements()]);
  },
  methods: {
    hasApplied(jobId) {
      return this.applications.some(app => app.job_id === jobId);
    },
    async loadJobs() {
      this.jobsLoading = true;
      try {
        const res = await fetchJobs();
        // Endpoint returns an array or an object with a message if none found
        if (Array.isArray(res.data)) {
          this.jobs = res.data;
        } else {
          this.jobs = []; // "No job found"
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
    async handleApply(jobId) {
      if (!confirm("Are you sure you want to apply for this job?")) return;
      this.applyingId = jobId;
      try {
        const res = await applyJob(jobId);
        alert(res.data.message || "Application submitted successfully");
        await this.loadApplications(); // Refresh history
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
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.dashboard-section h3 {
  font-size: 1.25rem;
  color: #2d3748;
  margin-bottom: 1rem;
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
