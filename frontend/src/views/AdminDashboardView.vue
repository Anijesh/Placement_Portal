<template>
  <div class="dashboard-page">
    <header class="dashboard-header">
      <div class="header-content">
        <h2>Admin Dashboard</h2>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </header>

    <main class="dashboard-main fade-in">
      

      <section class="dashboard-section">
        <h3>Platform Overview</h3>
        <div v-if="statsLoading" class="loading-state">Loading stats...</div>
        <div v-else class="stats-grid">
          <div class="stat-card">
            <span class="stat-value">{{ stats.students || 0 }}</span>
            <span class="stat-label">Total Students</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ stats.companies || 0 }}</span>
            <span class="stat-label">Total Companies</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ stats.jobs || 0 }}</span>
            <span class="stat-label">Total Jobs</span>
          </div>
          <div class="stat-card">
            <span class="stat-value">{{ stats.applications || 0 }}</span>
            <span class="stat-label">Total Applications</span>
          </div>
        </div>
      </section>


      <section class="dashboard-section">
        <div class="section-header-row">
          <h3>Companies</h3>
          <div class="search-wrapper">
            <input v-model="companySearch" @input="handleCompanySearch" type="text" placeholder="Search companies..." class="search-input" />
          </div>
        </div>
        <div v-if="companiesLoading" class="loading-state">Loading companies...</div>
        <div v-else-if="companies.length === 0" class="empty-state">No companies registered yet.</div>
        <div v-else class="card-list">
          <div v-for="company in companies" :key="company.id" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ company.name }}</h4>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>ID:</strong> {{ company.id }}</span>
                <span><strong>Name:</strong> {{ company.name }}</span>
                <span><strong>Industry:</strong> {{ company.industry }}</span>
                <span><strong>Location:</strong> {{ company.location }}</span>
                <span><strong>Approval Status:</strong> <span :class="['status-badge', company.status?.toLowerCase() || 'pending']">{{ company.status || 'pending' }}</span></span>
                <span><strong>Account Status:</strong> <span :class="['status-badge', company.is_active ? 'approved' : 'rejected']">{{ company.is_active ? 'Active' : 'Inactive' }}</span></span>
              </div>
            </div>
            <div class="card-footer actions">
              <button v-if="company.status !== 'approved'" @click="handleApproveCompany(company.id)" class="action-btn approve">Approve</button>
              <button v-if="company.status !== 'rejected'" @click="handleRejectCompany(company.id)" class="action-btn reject">Reject</button>
              <button v-if="!company.is_active" @click="handleActivateCompany(company.id)" class="action-btn secondary">Activate</button>
              <button v-if="company.is_active" @click="handleDeactivateCompany(company.id)" class="action-btn danger">Deactivate</button>
            </div>
          </div>
        </div>
      </section>


      <section class="dashboard-section">
        <div class="section-header-row">
          <h3>Students</h3>
          <div class="search-wrapper">
            <input v-model="studentSearch" @input="handleStudentSearch" type="text" placeholder="Search students..." class="search-input" />
          </div>
        </div>
        <div v-if="studentsLoading" class="loading-state">Loading students...</div>
        <div v-else-if="students.length === 0" class="empty-state">No students registered yet.</div>
        <div v-else class="card-list">
          <div v-for="student in students" :key="student.id" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ student.name }}</h4>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>ID:</strong> {{ student.id }}</span>
                <span><strong>Name:</strong> {{ student.name }}</span>
                <span><strong>Email:</strong> {{ student.email }}</span>
                <span><strong>Branch:</strong> {{ student.branch }}</span>
                <span><strong>CGPA:</strong> {{ student.cgpa }}</span>
                <span><strong>Graduation Year:</strong> {{ student.graduation_year }}</span>
                <span><strong>Skills:</strong> {{ student.skills }}</span>
                <span><strong>Account Status:</strong> <span :class="['status-badge', student.is_active ? 'approved' : 'rejected']">{{ student.is_active ? 'Active' : 'Inactive' }}</span></span>
              </div>
            </div>
            <div class="card-footer actions">
              <button v-if="!student.is_active" @click="handleActivateStudent(student.id)" class="action-btn secondary">Activate</button>
              <button v-if="student.is_active" @click="handleDeactivateStudent(student.id)" class="action-btn danger">Deactivate</button>
            </div>
          </div>
        </div>
      </section>


      <section class="dashboard-section">
        <h3>Job Postings</h3>
        <div v-if="jobsLoading" class="loading-state">Loading jobs...</div>
        <div v-else-if="jobs.length === 0" class="empty-state">No jobs posted yet.</div>
        <div v-else class="card-list">
          <div v-for="job in jobs" :key="job.id" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ job.title }}</h4>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>Job ID:</strong> {{ job.id }}</span>
                <span><strong>Company:</strong> {{ job.company }}</span>
                <span><strong>Title:</strong> {{ job.title }}</span>
                <span><strong>Description:</strong> {{ job.description }}</span>
                <span><strong>Min CGPA:</strong> {{ job.min_cgpa }}</span>
                <span><strong>Salary:</strong> {{ job.salary }}</span>
                <span><strong>Deadline:</strong> {{ formatDate(job.deadline) }}</span>
                <span><strong>Status:</strong> <span :class="['status-badge', job.status?.toLowerCase() || 'pending']">{{ job.status || 'pending' }}</span></span>
              </div>
            </div>
            <div class="card-footer actions">
              <button v-if="job.status !== 'approved'" @click="handleApproveJob(job.id)" class="action-btn approve">Approve</button>
              <button v-if="job.status !== 'rejected'" @click="handleRejectJob(job.id)" class="action-btn reject">Reject</button>
            </div>
          </div>
        </div>
      </section>

 
      <section class="dashboard-section">
        <h3>Applications</h3>
        <div v-if="applicationsLoading" class="loading-state">Loading applications...</div>
        <div v-else-if="applications.length === 0" class="empty-state">No applications submitted.</div>
        <div v-else class="card-list">
          <div v-for="app in applications" :key="app.application_id" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ app.student_name }}</h4>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>Application ID:</strong> {{ app.application_id }}</span>
                <span><strong>Student Name:</strong> {{ app.student_name }}</span>
                <span><strong>Student Branch:</strong> {{ app.student_branch }}</span>
                <span><strong>Company:</strong> {{ app.company }}</span>
                <span><strong>Job Title:</strong> {{ app.job_title }}</span>
                <span><strong>Offered Salary:</strong> {{ app.offered_salary }}</span>
                <span><strong>Status:</strong> <span :class="['status-badge', app.status?.toLowerCase() || 'pending']">{{ app.status || 'pending' }}</span></span>
              </div>
            </div>
          </div>
        </div>
      </section>


      <section class="dashboard-section">
        <h3>Placements</h3>
        <div v-if="placementsLoading" class="loading-state">Loading placements...</div>
        <div v-else-if="placements.length === 0" class="empty-state">No placements yet.</div>
        <div v-else class="card-list">
          <div v-for="(p, index) in placements" :key="index" class="card">
            <div class="card-header">
              <h4 class="company-name">{{ p.student_name }}</h4>
            </div>
            <div class="card-body">
              <div class="job-details">
                <span><strong>Application ID:</strong> {{ p.application_id }}</span>
                <span><strong>Student Name:</strong> {{ p.student_name }}</span>
                <span><strong>Company Name:</strong> {{ p.company_name }}</span>
                <span><strong>Job Title:</strong> {{ p.job_title }}</span>
                <span><strong>Offered Salary:</strong> {{ p.offered_salary }}</span>
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
import { 
  fetchStats, 
  fetchCompanies, approveCompany, rejectCompany, activateCompany, deactivateCompany, searchCompanies,
  fetchStudents, activateStudent, deactivateStudent, searchStudents,
  fetchJobs, approveJob, rejectJob,
  fetchApplications, fetchPlacements 
} from '../api/admin';
import { logoutAPI } from '../api/auth';

export default {
  data() {
    return {
      stats: {},
      companies: [],
      students: [],
      jobs: [],
      applications: [],
      placements: [],
      companySearch: "",
      studentSearch: "",
      searchTimeout: null,
      statsLoading: true,
      companiesLoading: true,
      studentsLoading: true,
      jobsLoading: true,
      applicationsLoading: true,
      placementsLoading: true,
    };
  },
  async created() {
    this.loadAllData();
  },
  methods: {
    async loadAllData() {
      await Promise.allSettled([
        this.loadStats(),
        this.loadCompanies(),
        this.loadStudents(),
        this.loadJobs(),
        this.loadApplications(),
        this.loadPlacements()
      ]);
    },
    async loadStats() {
      this.statsLoading = true;
      try {
        const res = await fetchStats();
        this.stats = res.data;
      } catch (err) {
        console.error("Failed to fetch stats:", err);
      } finally {
        this.statsLoading = false;
      }
    },
    async loadCompanies() {
      this.companiesLoading = true;
      try {
        const res = await fetchCompanies();
        this.companies = res.data;
      } catch (err) {
        console.error("Failed to fetch companies:", err);
      } finally {
        this.companiesLoading = false;
      }
    },
    async loadStudents() {
      this.studentsLoading = true;
      try {
        const res = await fetchStudents();
        this.students = res.data;
      } catch (err) {
        console.error("Failed to fetch students:", err);
      } finally {
        this.studentsLoading = false;
      }
    },
    async loadJobs() {
      this.jobsLoading = true;
      try {
        const res = await fetchJobs();
        this.jobs = res.data;
      } catch (err) {
        console.error("Failed to fetch jobs:", err);
      } finally {
        this.jobsLoading = false;
      }
    },
    async loadApplications() {
      this.applicationsLoading = true;
      try {
        const res = await fetchApplications();
        this.applications = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        console.error("Failed to fetch applications:", err);
      } finally {
        this.applicationsLoading = false;
      }
    },
    async loadPlacements() {
      this.placementsLoading = true;
      try {
        const res = await fetchPlacements();
        this.placements = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        console.error("Failed to fetch placements:", err);
      } finally {
        this.placementsLoading = false;
      }
    },
    
    handleCompanySearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(async () => {
        if (!this.companySearch.trim()) {
          this.loadCompanies();
          return;
        }
        this.companiesLoading = true;
        try {
          const res = await searchCompanies(this.companySearch);
          this.companies = res.data;
        } catch (err) {
          console.error("Search failed:", err);
        } finally {
          this.companiesLoading = false;
        }
      }, 300);
    },
    handleStudentSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(async () => {
        if (!this.studentSearch.trim()) {
          this.loadStudents();
          return;
        }
        this.studentsLoading = true;
        try {
          const res = await searchStudents(this.studentSearch);
          this.students = res.data;
        } catch (err) {
          console.error("Search failed:", err);
        } finally {
          this.studentsLoading = false;
        }
      }, 300);
    },
    
  
    async handleApproveCompany(id) {
      if (!confirm("Approve this company?")) return;
      try {
        await approveCompany(id);
        this.loadCompanies();
      } catch (err) {
        alert("Action failed.");
      }
    },
    async handleRejectCompany(id) {
      if (!confirm("Reject this company?")) return;
      try {
        await rejectCompany(id);
        this.loadCompanies();
      } catch (err) {
        alert("Action failed.");
      }
    },
    async handleActivateCompany(id) {
      if (!confirm("Activate this company account?")) return;
      try {
        await activateCompany(id);
        alert("Company Activated");
        this.loadCompanies();
      } catch (err) {
        alert("Action failed.");
      }
    },
    async handleDeactivateCompany(id) {
      if (!confirm("Deactivate this company account?")) return;
      try {
        await deactivateCompany(id);
        alert("Company Deactivated");
        this.loadCompanies();
      } catch (err) {
        alert("Action failed.");
      }
    },


    async handleActivateStudent(id) {
      if (!confirm("Activate this student account?")) return;
      try {
        await activateStudent(id);
        alert("Student Activated");
        this.loadStudents();
      } catch (err) {
        alert("Action failed.");
      }
    },
    async handleDeactivateStudent(id) {
      if (!confirm("Deactivate this student account?")) return;
      try {
        await deactivateStudent(id);
        alert("Student Deactivated");
        this.loadStudents();
      } catch (err) {
        alert("Action failed.");
      }
    },


    async handleApproveJob(id) {
      if (!confirm("Approve this job posting?")) return;
      try {
        await approveJob(id);
        this.loadJobs();
      } catch (err) {
        alert("Action failed.");
      }
    },
    async handleRejectJob(id) {
      if (!confirm("Reject this job posting?")) return;
      try {
        await rejectJob(id);
        this.loadJobs();
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
  margin-bottom: 1rem;
  font-weight: 600;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
}

.section-header-row h3 {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.search-input {
  padding: 0.5rem 0.8rem;
  border-radius: 6px;
  border: 1px solid #cbd5e0;
  background: #fff;
  color: #2d3748;
  font-size: 0.9rem;
  min-width: 250px;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid #edf2f7;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #3182ce;
}

.stat-label {
  font-size: 1rem;
  color: #718096;
  margin-top: 0.5rem;
  font-weight: 500;
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

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem;
  border-radius: 6px;
  border: none;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  text-align: center;
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

.action-btn.danger {
  background: #fed7d7;
  color: #c53030;
}
.action-btn.danger:hover { background: #feb2b2; }


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

.status-badge.approved, .status-badge.accepted, .status-badge.selected {
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

