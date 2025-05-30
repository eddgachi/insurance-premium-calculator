<!-- views/QuoteRequestsView.vue -->
<template>
  <div class="quote-requests-view">
    <!-- Header Section -->
    <div class="page-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h3 mb-2 fw-bold text-primary">
            <i class="fas fa-file-invoice me-2"></i>
            Quote Requests
          </h1>
          <p class="text-muted mb-0">Manage and track all your insurance quote requests</p>
        </div>
        <div class="col-md-4 text-md-end">
          <div class="d-flex gap-2 justify-content-md-end">
            <button @click="refreshData" class="btn btn-outline-primary btn-sm" :disabled="loading">
              <i class="fas fa-sync-alt me-1" :class="{ 'fa-spin': loading }"></i>
              Refresh
            </button>
            <router-link to="/" class="btn btn-primary btn-sm">
              <i class="fas fa-plus me-1"></i>
              New Quote
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section mb-4">
      <div class="card border-0 shadow-sm">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label fw-semibold">Search</label>
              <div class="input-group">
                <span class="input-group-text">
                  <i class="fas fa-search"></i>
                </span>
                <input
                  v-model="filters.search"
                  type="text"
                  class="form-control"
                  placeholder="Search by location, policy type..."
                  @input="applyFilters"
                />
              </div>
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold">Policy Type</label>
              <select v-model="filters.policyType" @change="applyFilters" class="form-select">
                <option value="">All Types</option>
                <option value="auto">Auto</option>
                <option value="home">Home</option>
                <option value="life">Life</option>
                <option value="health">Health</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold">Date Range</label>
              <select v-model="filters.dateRange" @change="applyFilters" class="form-select">
                <option value="">All Time</option>
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
                <option value="quarter">This Quarter</option>
              </select>
            </div>
            <div class="col-md-2">
              <label class="form-label fw-semibold">Sort By</label>
              <select v-model="filters.sortBy" @change="applyFilters" class="form-select">
                <option value="date_desc">Newest First</option>
                <option value="date_asc">Oldest First</option>
                <option value="coverage_desc">Highest Coverage</option>
                <option value="coverage_asc">Lowest Coverage</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Stats -->
    <div class="summary-stats mb-4">
      <div class="row g-3">
        <div class="col-md-3">
          <div class="stat-card bg-primary text-white">
            <div class="stat-content">
              <div class="stat-number">{{ filteredRequests.length }}</div>
              <div class="stat-label">Total Requests</div>
            </div>
            <div class="stat-icon">
              <i class="fas fa-file-invoice"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-success text-white">
            <div class="stat-content">
              <div class="stat-number">{{ completedCount }}</div>
              <div class="stat-label">Completed</div>
            </div>
            <div class="stat-icon">
              <i class="fas fa-check-circle"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-warning text-white">
            <div class="stat-content">
              <div class="stat-number">{{ pendingCount }}</div>
              <div class="stat-label">Pending</div>
            </div>
            <div class="stat-icon">
              <i class="fas fa-clock"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-info text-white">
            <div class="stat-content">
              <div class="stat-number">${{ averageCoverage }}</div>
              <div class="stat-label">Avg Coverage</div>
            </div>
            <div class="stat-icon">
              <i class="fas fa-shield-alt"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Loading quote requests...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredRequests.length === 0" class="empty-state text-center py-5">
        <div class="empty-icon mb-4">
          <i class="fas fa-inbox fa-4x text-muted"></i>
        </div>
        <h4 class="text-muted mb-3">No Quote Requests Found</h4>
        <p class="text-muted mb-4">
          {{
            filters.search || filters.policyType || filters.dateRange
              ? 'No requests match your current filters.'
              : "You haven't created any quote requests yet."
          }}
        </p>
        <div class="d-flex gap-2 justify-content-center">
          <router-link to="/" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>
            Create First Quote
          </router-link>
          <button v-if="hasFilters" @click="clearFilters" class="btn btn-outline-secondary">
            <i class="fas fa-times me-2"></i>
            Clear Filters
          </button>
        </div>
      </div>

      <!-- Requests Table -->
      <div v-else class="table-container">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-light border-0">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">Quote Requests ({{ filteredRequests.length }})</h5>
              <div class="table-actions">
                <button @click="exportToCSV" class="btn btn-outline-success btn-sm">
                  <i class="fas fa-download me-1"></i>
                  Export CSV
                </button>
                <button @click="bulkDelete" class="btn btn-outline-danger btn-sm" v-if="selectedRequests.length > 0">
                  <i class="fas fa-trash me-1"></i>
                  Delete Selected ({{ selectedRequests.length }})
                </button>
              </div>
            </div>
          </div>
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th class="border-0">
                    <div class="form-check">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        :checked="allSelected"
                        @change="toggleSelectAll"
                      />
                    </div>
                  </th>
                  <th class="border-0">ID</th>
                  <th class="border-0">Policy Type</th>
                  <th class="border-0">Customer</th>
                  <th class="border-0">Coverage</th>
                  <th class="border-0">Location</th>
                  <th class="border-0">Status</th>
                  <th class="border-0">Date</th>
                  <th class="border-0">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in paginatedRequests" :key="request.id" class="table-row">
                  <td>
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" :value="request.id" v-model="selectedRequests" />
                    </div>
                  </td>
                  <td>
                    <span class="fw-semibold">#{{ request.id }}</span>
                  </td>
                  <td>
                    <div class="policy-type">
                      <span class="policy-icon">{{ getPolicyIcon(request.policy_type) }}</span>
                      <span class="policy-name">{{ formatPolicyType(request.policy_type) }}</span>
                    </div>
                  </td>
                  <td>
                    <div class="customer-info">
                      <div class="customer-name">{{ request.customer_name || 'Anonymous' }}</div>
                      <div class="customer-age text-muted">Age: {{ request.age }}</div>
                    </div>
                  </td>
                  <td>
                    <span class="coverage-amount">${{ formatCurrency(request.coverage) }}</span>
                  </td>
                  <td>
                    <span class="location">
                      <i class="fas fa-map-marker-alt text-muted me-1"></i>
                      {{ request.location }}
                    </span>
                  </td>
                  <td>
                    <span class="badge" :class="getStatusBadge(request.status)">
                      {{ request.status || 'pending' }}
                    </span>
                  </td>
                  <td>
                    <div class="date-info">
                      <div class="date">{{ formatDate(request.requested_at) }}</div>
                      <div class="time text-muted">{{ formatTime(request.requested_at) }}</div>
                    </div>
                  </td>
                  <td>
                    <div class="action-buttons">
                      <button @click="viewRequest(request)" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button @click="editRequest(request)" class="btn btn-sm btn-outline-secondary">
                        <i class="fas fa-edit"></i>
                      </button>
                      <button @click="deleteRequest(request)" class="btn btn-sm btn-outline-danger">
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="card-footer bg-light border-0" v-if="totalPages > 1">
            <nav aria-label="Requests pagination">
              <ul class="pagination justify-content-center mb-0">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <button class="page-link" @click="currentPage = 1" :disabled="currentPage === 1">
                    <i class="fas fa-angle-double-left"></i>
                  </button>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <button class="page-link" @click="currentPage--" :disabled="currentPage === 1">
                    <i class="fas fa-angle-left"></i>
                  </button>
                </li>
                <li
                  v-for="page in visiblePages"
                  :key="page"
                  class="page-item"
                  :class="{ active: page === currentPage }"
                >
                  <button class="page-link" @click="currentPage = page">{{ page }}</button>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <button class="page-link" @click="currentPage++" :disabled="currentPage === totalPages">
                    <i class="fas fa-angle-right"></i>
                  </button>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <button class="page-link" @click="currentPage = totalPages" :disabled="currentPage === totalPages">
                    <i class="fas fa-angle-double-right"></i>
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'QuoteRequestsView',
  data() {
    return {
      requests: [],
      loading: true,
      filters: {
        search: '',
        policyType: '',
        dateRange: '',
        sortBy: 'date_desc',
      },
      selectedRequests: [],
      currentPage: 1,
      itemsPerPage: 10,
    }
  },
  computed: {
    filteredRequests() {
      let filtered = [...this.requests]

      // Apply search filter
      if (this.filters.search) {
        const search = this.filters.search.toLowerCase()
        filtered = filtered.filter(
          (req) =>
            req.location.toLowerCase().includes(search) ||
            req.policy_type.toLowerCase().includes(search) ||
            req.id.toString().includes(search)
        )
      }

      // Apply policy type filter
      if (this.filters.policyType) {
        filtered = filtered.filter((req) => req.policy_type === this.filters.policyType)
      }

      // Apply date range filter
      if (this.filters.dateRange) {
        const now = new Date()
        const filterDate = new Date()

        switch (this.filters.dateRange) {
          case 'today':
            filterDate.setHours(0, 0, 0, 0)
            break
          case 'week':
            filterDate.setDate(now.getDate() - 7)
            break
          case 'month':
            filterDate.setMonth(now.getMonth() - 1)
            break
          case 'quarter':
            filterDate.setMonth(now.getMonth() - 3)
            break
        }

        filtered = filtered.filter((req) => new Date(req.requested_at) >= filterDate)
      }

      // Apply sorting
      filtered.sort((a, b) => {
        switch (this.filters.sortBy) {
          case 'date_desc':
            return new Date(b.requested_at) - new Date(a.requested_at)
          case 'date_asc':
            return new Date(a.requested_at) - new Date(b.requested_at)
          case 'coverage_desc':
            return b.coverage - a.coverage
          case 'coverage_asc':
            return a.coverage - b.coverage
          default:
            return 0
        }
      })

      return filtered
    },

    paginatedRequests() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredRequests.slice(start, end)
    },

    totalPages() {
      return Math.ceil(this.filteredRequests.length / this.itemsPerPage)
    },

    visiblePages() {
      const pages = []
      const start = Math.max(1, this.currentPage - 2)
      const end = Math.min(this.totalPages, this.currentPage + 2)

      for (let i = start; i <= end; i++) {
        pages.push(i)
      }

      return pages
    },

    completedCount() {
      return this.filteredRequests.filter((req) => req.status === 'completed').length
    },

    pendingCount() {
      return this.filteredRequests.filter((req) => req.status === 'pending' || !req.status).length
    },

    averageCoverage() {
      if (this.filteredRequests.length === 0) return '0'
      const avg = this.filteredRequests.reduce((sum, req) => sum + req.coverage, 0) / this.filteredRequests.length
      return this.formatCurrency(avg)
    },

    allSelected() {
      return this.selectedRequests.length === this.paginatedRequests.length && this.paginatedRequests.length > 0
    },

    hasFilters() {
      return this.filters.search || this.filters.policyType || this.filters.dateRange
    },
  },
  async mounted() {
    await this.loadRequests()
  },
  methods: {
    async loadRequests() {
      this.loading = true
      try {
        const res = await api.get('/requests')
        this.requests = res.data
      } catch (err) {
        console.error('Failed to load requests:', err)
        // Mock data for demonstration
        this.requests = [
          {
            id: 1,
            policy_type: 'auto',
            age: 30,
            coverage: 100000,
            location: 'New York, NY',
            requested_at: new Date().toISOString(),
            status: 'completed',
            customer_name: 'John Doe',
          },
          {
            id: 2,
            policy_type: 'home',
            age: 45,
            coverage: 250000,
            location: 'Los Angeles, CA',
            requested_at: new Date(Date.now() - 86400000).toISOString(),
            status: 'pending',
            customer_name: 'Jane Smith',
          },
        ]
      } finally {
        this.loading = false
      }
    },

    async refreshData() {
      await this.loadRequests()
    },

    applyFilters() {
      this.currentPage = 1
    },

    clearFilters() {
      this.filters = {
        search: '',
        policyType: '',
        dateRange: '',
        sortBy: 'date_desc',
      }
      this.currentPage = 1
    },

    toggleSelectAll() {
      if (this.allSelected) {
        this.selectedRequests = []
      } else {
        this.selectedRequests = this.paginatedRequests.map((req) => req.id)
      }
    },

    viewRequest(request) {
      // Navigate to request details
      this.$router.push(`/requests/${request.id}`)
    },

    editRequest(request) {
      // Navigate to edit form
      this.$router.push(`/requests/${request.id}/edit`)
    },

    async deleteRequest(request) {
      if (confirm(`Are you sure you want to delete request #${request.id}?`)) {
        try {
          await api.delete(`/requests/${request.id}`)
          await this.loadRequests()
        } catch (err) {
          alert('Failed to delete request')
        }
      }
    },

    async bulkDelete() {
      if (confirm(`Are you sure you want to delete ${this.selectedRequests.length} selected requests?`)) {
        try {
          await Promise.all(this.selectedRequests.map((id) => api.delete(`/requests/${id}`)))
          this.selectedRequests = []
          await this.loadRequests()
        } catch (err) {
          alert('Failed to delete some requests')
        }
      }
    },

    exportToCSV() {
      const headers = ['ID', 'Policy Type', 'Age', 'Coverage', 'Location', 'Status', 'Date']
      const data = this.filteredRequests.map((req) => [
        req.id,
        req.policy_type,
        req.age,
        req.coverage,
        req.location,
        req.status || 'pending',
        this.formatDate(req.requested_at),
      ])

      const csvContent = [headers, ...data].map((row) => row.map((cell) => `"${cell}"`).join(',')).join('\n')

      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `quote-requests-${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      URL.revokeObjectURL(url)
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat('en-US').format(amount)
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString()
    },

    formatTime(dateStr) {
      return new Date(dateStr).toLocaleTimeString()
    },

    formatPolicyType(type) {
      const types = {
        auto: 'Auto Insurance',
        home: 'Home Insurance',
        life: 'Life Insurance',
        health: 'Health Insurance',
      }
      return types[type] || type
    },

    getPolicyIcon(type) {
      const icons = {
        auto: '🚗',
        home: '🏠',
        life: '👤',
        health: '🏥',
      }
      return icons[type] || '📄'
    },

    getStatusBadge(status) {
      const badges = {
        completed: 'bg-success',
        pending: 'bg-warning',
        failed: 'bg-danger',
        processing: 'bg-info',
      }
      return badges[status] || 'bg-secondary'
    },
  },
}
</script>

<style scoped>
.quote-requests-view {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  padding: 1rem 0;
}

.stat-card {
  background: linear-gradient(135deg, var(--bs-primary) 0%, var(--bs-primary-rgb) 100%);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: between;
  align-items: center;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-content {
  flex-grow: 1;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-icon {
  font-size: 2rem;
  opacity: 0.7;
}

.table-container .card {
  border-radius: 12px;
  overflow: hidden;
}

.table {
  font-size: 0.9rem;
}

.table-row:hover {
  background-color: rgba(13, 110, 253, 0.05);
}

.policy-type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.policy-icon {
  font-size: 1.2rem;
}

.customer-info .customer-name {
  font-weight: 500;
}

.customer-info .customer-age {
  font-size: 0.8rem;
}

.coverage-amount {
  font-weight: 600;
  color: #198754;
}

.date-info .date {
  font-weight: 500;
}

.date-info .time {
  font-size: 0.8rem;
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.action-buttons .btn {
  padding: 0.25rem 0.5rem;
}

.empty-state .empty-icon {
  color: #dee2e6;
}

.badge {
  font-size: 0.75rem;
  padding: 0.4rem 0.8rem;
  text-transform: capitalize;
}

@media (max-width: 768px) {
  .stat-card {
    text-align: center;
  }

  .table-responsive {
    font-size: 0.8rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 0.1rem;
  }

  .customer-info,
  .date-info {
    font-size: 0.8rem;
  }
}
</style>
