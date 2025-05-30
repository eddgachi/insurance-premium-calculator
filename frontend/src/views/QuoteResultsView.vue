<!-- views/QuoteResultsView.vue -->
<template>
  <div class="quote-results-view">
    <!-- Header Section -->
    <div class="page-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h3 mb-2 fw-bold text-primary">
            <i class="fas fa-chart-line me-2"></i>
            Quote Results
          </h1>
          <p class="text-muted mb-0">View and analyze all your insurance quote results</p>
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
                  placeholder="Search by ID, premium amount..."
                  @input="applyFilters"
                />
              </div>
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold">Premium Range</label>
              <select v-model="filters.premiumRange" @change="applyFilters" class="form-select">
                <option value="">All Premiums</option>
                <option value="low">Under $500</option>
                <option value="medium">$500 - $1,500</option>
                <option value="high">Over $1,500</option>
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
                <option value="premium_desc">Highest Premium</option>
                <option value="premium_asc">Lowest Premium</option>
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
              <div class="stat-number">{{ filteredResults.length }}</div>
              <div class="stat-label">Total Results</div>
            </div>
            <div class="stat-icon">
              <i class="fas fa-chart-line"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-success text-white">
            <div class="stat-content">
              <div class="stat-number">${{ averagePremium }}</div>
              <div class="stat-label">Avg Premium</div>
            </div>
            <div class="stat-icon">
              <i class="fas fa-dollar-sign"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-warning text-white">
            <div class="stat-content">
              <div class="stat-number">${{ lowestPremium }}</div>
              <div class="stat-label">Lowest Premium</div>
            </div>
            <div class="stat-icon">
              <i class="fas fa-arrow-down"></i>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-info text-white">
            <div class="stat-content">
              <div class="stat-number">${{ highestPremium }}</div>
              <div class="stat-label">Highest Premium</div>
            </div>
            <div class="stat-icon">
              <i class="fas fa-arrow-up"></i>
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
        <p class="mt-3 text-muted">Loading quote results...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredResults.length === 0" class="empty-state text-center py-5">
        <div class="empty-icon mb-4">
          <i class="fas fa-chart-line fa-4x text-muted"></i>
        </div>
        <h4 class="text-muted mb-3">No Quote Results Found</h4>
        <p class="text-muted mb-4">
          {{
            filters.search || filters.premiumRange || filters.dateRange
              ? 'No results match your current filters.'
              : 'No quote results are available yet.'
          }}
        </p>
        <div class="d-flex gap-2 justify-content-center">
          <router-link to="/" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>
            Get New Quote
          </router-link>
          <button v-if="hasFilters" @click="clearFilters" class="btn btn-outline-secondary">
            <i class="fas fa-times me-2"></i>
            Clear Filters
          </button>
        </div>
      </div>

      <!-- Results Table -->
      <div v-else class="table-container">
        <div class="card border-0 shadow-sm">
          <div class="card-header bg-light border-0">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">Quote Results ({{ filteredResults.length }})</h5>
              <div class="table-actions">
                <button @click="exportToCSV" class="btn btn-outline-success btn-sm">
                  <i class="fas fa-download me-1"></i>
                  Export CSV
                </button>
                <button @click="bulkDelete" class="btn btn-outline-danger btn-sm" v-if="selectedResults.length > 0">
                  <i class="fas fa-trash me-1"></i>
                  Delete Selected ({{ selectedResults.length }})
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
                  <th class="border-0">Result ID</th>
                  <th class="border-0">Request ID</th>
                  <th class="border-0">Premium</th>
                  <th class="border-0">Coverage Amount</th>
                  <th class="border-0">Provider</th>
                  <th class="border-0">Status</th>
                  <th class="border-0">Fetched At</th>
                  <th class="border-0">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="result in paginatedResults" :key="result.id" class="table-row">
                  <td>
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" :value="result.id" v-model="selectedResults" />
                    </div>
                  </td>
                  <td>
                    <span class="fw-semibold">#{{ result.id }}</span>
                  </td>
                  <td>
                    <router-link :to="`/requests/${result.request_id}`" class="text-decoration-none">
                      <span class="fw-semibold text-primary">#{{ result.request_id }}</span>
                    </router-link>
                  </td>
                  <td>
                    <span class="premium-amount">${{ formatCurrency(result.premium) }}</span>
                  </td>
                  <td>
                    <span class="coverage-amount">${{ formatCurrency(result.coverage_amount) }}</span>
                  </td>
                  <td>
                    <div class="provider-info">
                      <span class="provider-name">{{ result.provider || 'Unknown' }}</span>
                      <div class="provider-rating text-muted">
                        <i class="fas fa-star"></i>
                        {{ result.rating || 'N/A' }}
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="badge" :class="getStatusBadge(result.status)">
                      {{ result.status || 'active' }}
                    </span>
                  </td>
                  <td>
                    <div class="date-info">
                      <div class="date">{{ formatDate(result.fetched_at) }}</div>
                      <div class="time text-muted">{{ formatTime(result.fetched_at) }}</div>
                    </div>
                  </td>
                  <td>
                    <div class="action-buttons">
                      <button @click="viewResult(result)" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button @click="compareResult(result)" class="btn btn-sm btn-outline-info">
                        <i class="fas fa-balance-scale"></i>
                      </button>
                      <button @click="deleteResult(result)" class="btn btn-sm btn-outline-danger">
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
            <nav aria-label="Results pagination">
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
  name: 'QuoteResultsView',
  data() {
    return {
      results: [],
      loading: true,
      filters: {
        search: '',
        premiumRange: '',
        dateRange: '',
        sortBy: 'date_desc',
      },
      selectedResults: [],
      currentPage: 1,
      itemsPerPage: 10,
    }
  },
  computed: {
    filteredResults() {
      let filtered = [...this.results]

      // Apply search filter
      if (this.filters.search) {
        const search = this.filters.search.toLowerCase()
        filtered = filtered.filter(
          (result) =>
            result.id.toString().includes(search) ||
            result.request_id.toString().includes(search) ||
            result.premium.toString().includes(search) ||
            (result.provider && result.provider.toLowerCase().includes(search))
        )
      }

      // Apply premium range filter
      if (this.filters.premiumRange) {
        filtered = filtered.filter((result) => {
          const premium = result.premium
          switch (this.filters.premiumRange) {
            case 'low':
              return premium < 500
            case 'medium':
              return premium >= 500 && premium <= 1500
            case 'high':
              return premium > 1500
            default:
              return true
          }
        })
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

        filtered = filtered.filter((result) => new Date(result.fetched_at) >= filterDate)
      }

      // Apply sorting
      filtered.sort((a, b) => {
        switch (this.filters.sortBy) {
          case 'date_desc':
            return new Date(b.fetched_at) - new Date(a.fetched_at)
          case 'date_asc':
            return new Date(a.fetched_at) - new Date(b.fetched_at)
          case 'premium_desc':
            return b.premium - a.premium
          case 'premium_asc':
            return a.premium - b.premium
          default:
            return 0
        }
      })

      return filtered
    },

    paginatedResults() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredResults.slice(start, end)
    },

    totalPages() {
      return Math.ceil(this.filteredResults.length / this.itemsPerPage)
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

    averagePremium() {
      if (this.filteredResults.length === 0) return '0'
      const avg = this.filteredResults.reduce((sum, result) => sum + result.premium, 0) / this.filteredResults.length
      return this.formatCurrency(avg)
    },

    lowestPremium() {
      if (this.filteredResults.length === 0) return '0'
      const min = Math.min(...this.filteredResults.map((result) => result.premium))
      return this.formatCurrency(min)
    },

    highestPremium() {
      if (this.filteredResults.length === 0) return '0'
      const max = Math.max(...this.filteredResults.map((result) => result.premium))
      return this.formatCurrency(max)
    },

    allSelected() {
      return this.selectedResults.length === this.paginatedResults.length && this.paginatedResults.length > 0
    },

    hasFilters() {
      return this.filters.search || this.filters.premiumRange || this.filters.dateRange
    },
  },
  async mounted() {
    await this.loadResults()
  },
  methods: {
    async loadResults() {
      this.loading = true
      try {
        const res = await api.get('/results')
        this.results = res.data
      } catch (err) {
        console.error('Failed to load results:', err)
        // Mock data for demonstration
        this.results = [
          {
            id: 1,
            request_id: 1,
            premium: 1200.5,
            coverage_amount: 100000,
            provider: 'SafeGuard Insurance',
            rating: 4.5,
            status: 'active',
            fetched_at: new Date().toISOString(),
          },
          {
            id: 2,
            request_id: 2,
            premium: 850.75,
            coverage_amount: 250000,
            provider: 'SecureLife Corp',
            rating: 4.2,
            status: 'expired',
            fetched_at: new Date(Date.now() - 86400000).toISOString(),
          },
        ]
      } finally {
        this.loading = false
      }
    },

    async refreshData() {
      await this.loadResults()
    },

    applyFilters() {
      this.currentPage = 1
    },

    clearFilters() {
      this.filters = {
        search: '',
        premiumRange: '',
        dateRange: '',
        sortBy: 'date_desc',
      }
      this.currentPage = 1
    },

    toggleSelectAll() {
      if (this.allSelected) {
        this.selectedResults = []
      } else {
        this.selectedResults = this.paginatedResults.map((result) => result.id)
      }
    },

    viewResult(result) {
      // Navigate to result details
      this.$router.push(`/results/${result.id}`)
    },

    compareResult(result) {
      // Navigate to comparison view
      this.$router.push(`/compare/${result.id}`)
    },

    async deleteResult(result) {
      if (confirm(`Are you sure you want to delete result #${result.id}?`)) {
        try {
          await api.delete(`/results/${result.id}`)
          await this.loadResults()
        } catch (err) {
          alert('Failed to delete result')
        }
      }
    },

    async bulkDelete() {
      if (confirm(`Are you sure you want to delete ${this.selectedResults.length} selected results?`)) {
        try {
          await Promise.all(this.selectedResults.map((id) => api.delete(`/results/${id}`)))
          this.selectedResults = []
          await this.loadResults()
        } catch (err) {
          alert('Failed to delete some results')
        }
      }
    },

    exportToCSV() {
      const headers = ['ID', 'Request ID', 'Premium', 'Coverage', 'Provider', 'Rating', 'Status', 'Date']
      const data = this.filteredResults.map((result) => [
        result.id,
        result.request_id,
        result.premium,
        result.coverage_amount,
        result.provider || 'Unknown',
        result.rating || 'N/A',
        result.status || 'active',
        this.formatDate(result.fetched_at),
      ])

      const csvContent = [headers, ...data].map((row) => row.map((cell) => `"${cell}"`).join(',')).join('\n')

      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `quote-results-${new Date().toISOString().split('T')[0]}.csv`
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

    getStatusBadge(status) {
      const badges = {
        active: 'bg-success',
        expired: 'bg-warning',
        cancelled: 'bg-danger',
        pending: 'bg-info',
      }
      return badges[status] || 'bg-secondary'
    },
  },
}
</script>

<style scoped>
.quote-results-view {
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
  justify-content: space-between;
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

.premium-amount {
  font-weight: 600;
  color: #198754;
  font-size: 1.1rem;
}

.coverage-amount {
  font-weight: 500;
  color: #0d6efd;
}

.provider-info .provider-name {
  font-weight: 500;
}

.provider-info .provider-rating {
  font-size: 0.8rem;
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

  .provider-info,
  .date-info {
    font-size: 0.8rem;
  }
}
</style>
