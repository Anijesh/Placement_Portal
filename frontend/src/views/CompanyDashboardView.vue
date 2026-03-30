<template>
  <div class="dashboard-page">
    <header class="dashboard-header">
      <div class="header-content">
        <h2>Company Dashboard</h2>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </header>

    <main class="dashboard-main fade-in">
      

      <section class="dashboard-section create-job-section">
        <div class="section-header">
          <h3>Create Placement Drive</h3>
          <button @click="toggleCreateForm" class="action-btn secondary">
            {{ showCreateForm ? 'Cancel' : 'Add New Drive' }}
          </button>
        </div>
        
        <form v-if="showCreateForm" @submit.prevent="handleCreateJob" class="create-job-form slide-down">
          <div class="input-group">
            <label>Job Title</label>
            <input v-model="newJob.title" type="text" placeholder="e.g. Software Engineer" required />
          </div>
          
          <div class="input-group">
            <label>Job Description</label>
            <textarea v-model="newJob.description" rows="3" placeholder="Require skills, roles, responsibilities..." required></textarea>
          </div>
          
          <div class="row-group">
            <div class="input-group">
              <label>Min CGPA</label>
              <input v-model="newJob.min_cgpa" type="number" step="0.01" min="0" max="10" placeholder="e.g. 7.5" required />
            </div>
            <div class="input-group">
              <label>Salary Package</label>
              <input v-model="newJob.salary" type="text" placeholder="e.g. 12 LPA" required />
            </div>
            <div class="input-group">
              <label>Application Deadline</label>
              <input v-model="newJob.deadline" type="date" required />
            </div>
          </div>
          
          <button type="submit" class="submit-btn" :disabled="isCreating">
            <span v-if="isCreating" class="spinner"></span>
            <span v-else>Submit Drive</span>
          </button>
        </form>
      </section>

 
      <section class="dashboard-section">
        <h3>My Placement Drives</h3>
        <div v-if="jobsLoading" class="loading-state">Loading your drives...</div>
        <div v-else-if="jobs.length === 0" class="empty-state">You haven't posted any jobs yet.</div>
        <div v-else class="card-list">
          <div v-for="job in jobs" :key="job.id" class="card job-card">
            <div class="card-header">
              <h4 class="company-name">{{ job.title }}</h4>
              <span :class="['status-badge', job.status?.toLowerCase() || 'pending']">{{ job.status || 'pending' }}</span>
            </div>
            <div class="card-body">
              <p class="description">{{ job.description }}</p>
              <div class="job-details">
                <span><strong>Min CGPA:</strong> {{ job.min_cgpa }}</span>
                <span><strong>Salary:</strong> {{ job.salary }}</span>
                <span><strong>Deadline:</strong> {{ formatDate(job.deadline) }}</span>
              </div>
            </div>
            <div class="card-footer actions">
              <button @click="viewApplications(job.id, job.title)" class="action-btn secondary">View Applicants</button>
              <button v-if="job.status !== 'closed' && job.status !== 'rejected'" @click="handleCloseJob(job.id)" class="action-btn reject">Close Drive</button>
              <button v-if="job.status === 'closed'" @click="handleReopenJob(job.id)" class="action-btn approve">Reopen Drive</button>
            </div>
          </div>
        </div>
      </section>


      <section v-if="selectedJobId !== null" class="dashboard-section applications-section slide-down" ref="applicationsSection">
        <div class="section-header">
          <h3>Applicants for: {{ selectedJobTitle }}</h3>
          <button @click="closeApplications" class="action-btn close-btn">Close</button>
        </div>
        
        <div v-if="applicationsLoading" class="loading-state">Loading applicants...</div>
        <div v-else-if="applications.length === 0" class="empty-state">No applications for this drive yet.</div>
        <div v-else class="card-list">
          <div v-for="app in applications" :key="app.application_id" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ app.student }}</h4>
              <span :class="['status-badge', app.status?.toLowerCase() || 'applied']">{{ app.status || 'applied' }}</span>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>Job Title:</strong> {{ app.job_title }}</span>
                <span><strong>Offered Salary:</strong> {{ app.salary }}</span>
                <span><strong>Branch:</strong> {{ app.branch }}</span>
                <span><strong>CGPA:</strong> {{ app.cgpa }}</span>
                <span><strong>Grad Year:</strong> {{ app.graduation_year }}</span>
                <span><strong>Skills:</strong> {{ app.skills }}</span>
                <span><strong>Applied On:</strong> {{ formatDate(app.applied_at) }}</span>
                <span v-if="app.interview_date"><strong>Interview:</strong> {{ formatDate(app.interview_date) }}</span>
              </div>
            </div>
            <div class="card-footer actions">
              <div v-if="app.status === 'shortlisted'" class="interview-scheduler">
                <input v-model="interviewDates[app.application_id]" type="date" class="date-input" />
                <button @click="handleScheduleInterview(app.application_id)" class="action-btn approve" :disabled="!interviewDates[app.application_id]">Schedule Interview</button>
              </div>
              <button v-if="app.status === 'applied'" @click="handleShortlist(app.application_id)" class="action-btn approve">Shortlist</button>
              <button v-if="app.status === 'interview_scheduled' || app.status === 'shortlisted'" @click="handleAccept(app.application_id)" class="action-btn approve">Select / Hire</button>
              <button v-if="app.status !== 'rejected' && app.status !== 'selected'" @click="handleReject(app.application_id)" class="action-btn reject">Reject</button>
            </div>
          </div>
        </div>
      </section>

    </main>
  </div>
</template>

<script>
import { 
  createJob, 
  fetchJobs, 
  fetchApplications, 
  shortlistApplication, 
  rejectApplication, 
  acceptApplication,
  closeJob,
  reopenJob,
  scheduleInterview
} from '../api/company';
import { logoutAPI } from '../api/auth';

export default {
  data() {
    return {
      jobs: [],
      jobsLoading: true,
      
      showCreateForm: false,
      isCreating: false,
      newJob: {
        title: '',
        description: '',
        min_cgpa: '',
        salary: '',
        deadline: ''
      },

      selectedJobId: null,
      selectedJobTitle: '',
      applications: [],
      applicationsLoading: false,
      interviewDates: {},
    };
  },
  async created() {
    this.loadJobs();
  },
  methods: {
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
    
    toggleCreateForm() {
      this.showCreateForm = !this.showCreateForm;
    },

    async handleCreateJob() {
      this.isCreating = true;
      try {
        const payload = {
          ...this.newJob,
          min_cgpa: parseFloat(this.newJob.min_cgpa)
        };
        await createJob(payload);
        alert("Placement drive created successfully! Waiting for Admin approval.");
        this.newJob = { title: '', description: '', min_cgpa: '', salary: '', deadline: '' };
        this.showCreateForm = false;
        await this.loadJobs();
      } catch (err) {
        alert(err.response?.data?.message || "Failed to create placement drive");
      } finally {
        this.isCreating = false;
      }
    },

    async viewApplications(jobId, jobTitle) {
      this.selectedJobId = jobId;
      this.selectedJobTitle = jobTitle;
      this.applicationsLoading = true;
      try {
        const res = await fetchApplications(jobId);
        if (Array.isArray(res.data)) {
          this.applications = res.data;
        } else {
          this.applications = [];
        }
        

        this.$nextTick(() => {
          if (this.$refs.applicationsSection) {
            this.$refs.applicationsSection.scrollIntoView({ behavior: 'smooth' });
          }
        });
      } catch (err) {
        alert("Failed to fetch applications");
      } finally {
        this.applicationsLoading = false;
      }
    },
    
    closeApplications() {
      this.selectedJobId = null;
      this.selectedJobTitle = '';
      this.applications = [];
    },

    async handleShortlist(appId) {
      if (!confirm("Shortlist this candidate?")) return;
      try {
        await shortlistApplication(appId);
        this.viewApplications(this.selectedJobId, this.selectedJobTitle);
      } catch (err) {
        alert("Action failed.");
      }
    },

    async handleScheduleInterview(appId) {
      if (!this.interviewDates[appId]) {
        alert("Please select a date for the interview.");
        return;
      }
      try {
        const payload = { 
          interview_date: this.interviewDates[appId] 
        };
        await scheduleInterview(appId, payload);
        alert("Interview scheduled successfully.");
        this.viewApplications(this.selectedJobId, this.selectedJobTitle);
      } catch (err) {
        alert("Action failed. " + (err.response?.data?.message || err.message));
      }
    },

    async handleCloseJob(jobId) {
      if (!confirm("Are you sure you want to close this placement drive? Students will no longer be able to apply.")) return;
      try {
        await closeJob(jobId);
        await this.loadJobs();
      } catch (err) {
        alert("Action failed.");
      }
    },

    async handleReopenJob(jobId) {
      if (!confirm("Are you sure you want to reopen this placement drive?")) return;
      try {
        await reopenJob(jobId);
        await this.loadJobs();
      } catch (err) {
        alert("Action failed.");
      }
    },

    async handleReject(appId) {
      if (!confirm("Reject this candidate?")) return;
      try {
        await rejectApplication(appId);
        this.viewApplications(this.selectedJobId, this.selectedJobTitle);
      } catch (err) {
        alert("Action failed.");
      }
    },

    async handleAccept(appId) {
      if (!confirm("Confirm selection/hiring of this candidate?")) return;
      try {
        await acceptApplication(appId);
        this.viewApplications(this.selectedJobId, this.selectedJobTitle);
      } catch (err) {
        alert("Action failed.");
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
    },
    formatDateTime(dateString) {
      if (!dateString || dateString === 'None') return "N/A";
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleString(undefined, options);
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
  padding: 0 2rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.dashboard-section h3 {
  font-size: 1.25rem;
  color: #2d3748;
  margin: 0;
  font-weight: 600;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.8rem;
  margin-bottom: 1rem;
}

.create-job-section {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 10px;
  border: 1px solid #edf2f7;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.create-job-form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  margin-top: 1rem;
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

label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
}

input, textarea {
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

textarea {
  resize: vertical;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
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

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  border-radius: 6px;
  border: none;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  text-align: center;
}

.actions .action-btn {
  flex: 1;
}

.action-btn.approve {
  background: #48bb78;
  color: #fff;
}
.action-btn.approve:hover { background: #38a169; }

.action-btn.reject {
  background: #f56565;
  color: #fff;
}
.action-btn.reject:hover { background: #e53e3e; }

.action-btn.secondary {
  background: #edf2f7;
  color: #2d3748;
}
.action-btn.secondary:hover { background: #e2e8f0; }

.action-btn.close-btn {
  flex: 0 1 auto;
  background: #edf2f7;
  color: #4a5568;
  padding: 0.4rem 0.8rem;
}

.interview-scheduler {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.date-input {
  width: 100%;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #cbd5e0;
  font-size: 0.85rem;
}

.submit-btn {
  margin-top: 0.5rem;
  padding: 0.6rem 2rem;
  align-self: flex-start;
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

.status-badge.approved, .status-badge.selected {
  background: #c6f6d5;
  color: #38a169;
}

.status-badge.rejected {
  background: #fed7d7;
  color: #e53e3e;
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

.slide-down {
  animation: slideDown 0.3s ease-out forwards;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.applications-section {
  background: #fafafa;
  border-radius: 10px;
  padding: 1.5rem;
  border: 2px solid #e2e8f0;
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
