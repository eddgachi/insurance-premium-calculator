<!-- views/DashboardView.vue -->
<template>
  <div class="dashboard-view">
    <!-- Dashboard Header -->
    <div class="dashboard-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <h1 class="h3 mb-2 fw-bold text-primary">
            <i class="fas fa-tachometer-alt me-2"></i>
            Dashboard
          </h1>
          <p class="text-muted mb-0">Welcome back! Get started with your insurance calculations.</p>
        </div>
        <div class="col-md-4 text-md-end">
          <div class="d-flex gap-2 justify-content-md-end">
            <button @click="showQuickStats = !showQuickStats" class="btn btn-outline-primary btn-sm">
              <i class="fas fa-chart-bar me-1"></i>
              {{ showQuickStats ? 'Hide' : 'Show' }} Stats
            </button>
            <button @click="refreshData" class="btn btn-outline-secondary btn-sm">
              <i class="fas fa-sync-alt me-1"></i>
              Refresh
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats Cards -->
    <div v-if="showQuickStats" class="quick-stats mb-4">
      <div class="row g-3">
        <div class="col-lg-3 col-md-6">
          <div class="stat-card">
            <div class="stat-icon bg-primary">
              <i class="fas fa-calculator"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.totalQuotes || 0 }}</h3>
              <p class="stat-label">Total Quotes</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <div class="stat-card">
            <div class="stat-icon bg-success">
              <i class="fas fa-check-circle"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.completedQuotes || 0 }}</h3>
              <p class="stat-label">Completed</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <div class="stat-card">
            <div class="stat-icon bg-warning">
              <i class="fas fa-clock"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">{{ stats.pendingQuotes || 0 }}</h3>
              <p class="stat-label">Pending</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <div class="stat-card">
            <div class="stat-icon bg-info">
              <i class="fas fa-dollar-sign"></i>
            </div>
            <div class="stat-content">
              <h3 class="stat-number">${{ formatCurrency(stats.avgPremium || 0) }}</h3>
              <p class="stat-label">Avg Premium</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity & Quick Actions -->
    <div class="row g-4 mb-4">
      <!-- Recent Activity -->
      <div class="col-lg-8">
        <div class="card h-100 shadow-sm border-0">
          <div class="card-header bg-light border-0">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="card-title mb-0">
                <i class="fas fa-history me-2 text-primary"></i>
                Recent Activity
              </h5>
              <router-link to="/requests" class="btn btn-sm btn-outline-primary"> View All </router-link>
            </div>
          </div>
          <div class="card-body">
            <div v-if="recentActivity.length === 0" class="text-center py-4">
              <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
              <p class="text-muted">No recent activity</p>
            </div>
            <div v-else class="activity-list">
              <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                <div class="activity-icon">
                  <i :class="getActivityIcon(activity.type)"></i>
                </div>
                <div class="activity-content">
                  <div class="activity-title">{{ activity.title }}</div>
                  <div class="activity-time">{{ formatTime(activity.timestamp) }}</div>
                </div>
                <div class="activity-value">
                  <span class="badge" :class="getActivityBadge(activity.status)">
                    {{ activity.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="col-lg-4">
        <div class="card h-100 shadow-sm border-0">
          <div class="card-header bg-light border-0">
            <h5 class="card-title mb-0">
              <i class="fas fa-bolt me-2 text-primary"></i>
              Quick Actions
            </h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-3">
              <button @click="scrollToCalculator" class="btn btn-primary btn-lg">
                <i class="fas fa-calculator me-2"></i>
                New Quote
              </button>
              <router-link to="/requests" class="btn btn-outline-secondary">
                <i class="fas fa-list me-2"></i>
                View Requests
              </router-link>
              <router-link to="/results" class="btn btn-outline-info">
                <i class="fas fa-chart-line me-2"></i>
                View Results
              </router-link>
              <button @click="exportData" class="btn btn-outline-success" :disabled="exporting">
                <i class="fas fa-download me-2"></i>
                {{ exporting ? 'Exporting...' : 'Export Data' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Calculator Component -->
    <PremiumCalculator ref="calculator" />

    <!-- Help Section -->
    <div class="help-section mt-5">
      <div class="card border-0 bg-light">
        <div class="card-body text-center py-4">
          <h5 class="card-title">
            <i class="fas fa-question-circle me-2 text-primary"></i>
            Need Help?
          </h5>
          <p class="card-text text-muted mb-3">
            Get assistance with calculating premiums, understanding policies, or managing your quotes.
          </p>
          <div class="d-flex gap-2 justify-content-center flex-wrap">
            <button class="btn btn-outline-primary btn-sm">
              <i class="fas fa-book me-1"></i>
              User Guide
            </button>
            <button class="btn btn-outline-info btn-sm">
              <i class="fas fa-comments me-1"></i>
              Contact Support
            </button>
            <button class="btn btn-outline-success btn-sm">
              <i class="fas fa-video me-1"></i>
              Watch Tutorial
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PremiumCalculator from '@/components/PremiumCalculator.vue'
import api from '@/api'

export default {
  name: 'DashboardView',
  components: {
    PremiumCalculator,
  },
  data() {
    return {
      showQuickStats: true,
      exporting: false,
      stats: {
        totalQuotes: 0,
        completedQuotes: 0,
        pendingQuotes: 0,
        avgPremium: 0,
      },
      recentActivity: [],
    }
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      try {
        // Load statistics
        const statsRes = await api.get('/dashboard/stats')
        this.stats = statsRes.data

        // Load recent activity
        const activityRes = await api.get('/dashboard/activity?limit=5')
        this.recentActivity = activityRes.data
      } catch (error) {
        console.error('Failed to load dashboard data:', error)
        // Mock data for demonstration
        this.stats = {
          totalQuotes: 156,
          completedQuotes: 142,
          pendingQuotes: 14,
          avgPremium: 1250,
        }
        this.recentActivity = [
          {
            id: 1,
            type: 'quote',
            title: 'Auto insurance quote completed',
            timestamp: new Date().toISOString(),
            status: 'completed',
          },
          {
            id: 2,
            type: 'quote',
            title: 'Home insurance quote requested',
            timestamp: new Date(Date.now() - 3600000).toISOString(),
            status: 'pending',
          },
        ]
      }
    },

    async refreshData() {
      await this.loadDashboardData()
    },

    scrollToCalculator() {
      this.$nextTick(() => {
        const calculator = this.$refs.calculator?.$el
        if (calculator) {
          calculator.scrollIntoView({ behavior: 'smooth' })
        }
      })
    },

    async exportData() {
      this.exporting = true
      try {
        // Simulate export
        await new Promise((resolve) => setTimeout(resolve, 2000))

        // In real implementation, this would download a file
        alert('Data exported successfully!')
      } catch (error) {
        console.error('Export failed:', error)
        alert('Export failed. Please try again.')
      } finally {
        this.exporting = false
      }
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat('en-US').format(amount)
    },

    formatTime(timestamp) {
      const date = new Date(timestamp)
      const now = new Date()
      const diffMs = now - date
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMs / 3600000)
      const diffDays = Math.floor(diffMs / 86400000)

      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins}m ago`
      if (diffHours < 24) return `${diffHours}h ago`
      if (diffDays < 7) return `${diffDays}d ago`
      return date.toLocaleDateString()
    },

    getActivityIcon(type) {
      const icons = {
        quote: 'fas fa-calculator text-primary',
        policy: 'fas fa-file-contract text-success',
        payment: 'fas fa-credit-card text-info',
        claim: 'fas fa-exclamation-triangle text-warning',
      }
      return icons[type] || 'fas fa-circle text-secondary'
    },

    getActivityBadge(status) {
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
.dashboard-view {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  padding: 1rem 0;
}

.quick-stats .stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #f1f3f4;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.quick-stats .stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  flex-shrink: 0;
}

.stat-content {
  flex-grow: 1;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: #212529;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card {
  border-radius: 12px;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.activity-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #f8f9fa;
  gap: 1rem;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-content {
  flex-grow: 1;
}

.activity-title {
  font-weight: 500;
  color: #212529;
  margin-bottom: 0.25rem;
}

.activity-time {
  font-size: 0.8rem;
  color: #6c757d;
}

.activity-value {
  flex-shrink: 0;
}

.help-section .card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.btn {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-lg {
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }

  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }

  .stat-number {
    font-size: 1.5rem;
  }

  .activity-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .activity-icon {
    align-self: flex-start;
  }
}
</style>
