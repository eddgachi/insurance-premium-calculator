<!-- components/PremiumCalculator.vue -->
<template>
  <div class="premium-calculator">
    <!-- Header Section -->
    <div class="calculator-header mb-4">
      <h2 class="h4 mb-2 fw-bold text-primary">
        <i class="fas fa-calculator me-2"></i>
        Premium Calculator
      </h2>
      <p class="text-muted mb-0">Get instant quotes for your insurance needs</p>
    </div>

    <!-- Main Calculator Card -->
    <div class="card shadow-sm border-0">
      <div class="card-header bg-primary bg-gradient text-white">
        <h5 class="card-title mb-0">
          <i class="fas fa-shield-alt me-2"></i>
          Calculate Your Premium
        </h5>
      </div>

      <div class="card-body p-4">
        <form @submit.prevent="onSubmit" class="needs-validation" novalidate>
          <!-- Form Grid -->
          <div class="row g-4">
            <!-- Policy Type -->
            <div class="col-lg-6 col-md-6">
              <label class="form-label fw-semibold">
                <i class="fas fa-file-contract me-1 text-primary"></i>
                Policy Type *
              </label>
              <select
                v-model="form.policy_type"
                class="form-select form-select-lg"
                :class="{ 'is-invalid': errors.policy_type }"
                required
              >
                <option value="">Select Policy Type</option>
                <option value="auto">🚗 Auto Insurance</option>
                <option value="home">🏠 Home Insurance</option>
                <option value="life">👤 Life Insurance</option>
                <option value="health">🏥 Health Insurance</option>
              </select>
              <div v-if="errors.policy_type" class="invalid-feedback">
                {{ errors.policy_type }}
              </div>
            </div>

            <!-- Age -->
            <div class="col-lg-3 col-md-6">
              <label class="form-label fw-semibold">
                <i class="fas fa-birthday-cake me-1 text-primary"></i>
                Age *
              </label>
              <input
                v-model.number="form.age"
                type="number"
                min="18"
                max="100"
                class="form-control form-control-lg"
                :class="{ 'is-invalid': errors.age }"
                placeholder="e.g., 30"
                required
              />
              <div v-if="errors.age" class="invalid-feedback">
                {{ errors.age }}
              </div>
            </div>

            <!-- Risk Score -->
            <div class="col-lg-3 col-md-6">
              <label class="form-label fw-semibold">
                <i class="fas fa-chart-line me-1 text-primary"></i>
                Risk Level
              </label>
              <select v-model="form.risk_level" class="form-select form-select-lg">
                <option value="low">🟢 Low Risk</option>
                <option value="medium">🟡 Medium Risk</option>
                <option value="high">🔴 High Risk</option>
              </select>
            </div>

            <!-- Coverage Amount -->
            <div class="col-lg-6 col-md-6">
              <label class="form-label fw-semibold">
                <i class="fas fa-dollar-sign me-1 text-primary"></i>
                Coverage Amount *
              </label>
              <div class="input-group input-group-lg">
                <span class="input-group-text">$</span>
                <input
                  v-model.number="form.coverage"
                  type="number"
                  min="1000"
                  step="1000"
                  class="form-control"
                  :class="{ 'is-invalid': errors.coverage }"
                  placeholder="100,000"
                  required
                />
              </div>
              <div class="form-text">Minimum coverage: $1,000</div>
              <div v-if="errors.coverage" class="invalid-feedback">
                {{ errors.coverage }}
              </div>
            </div>

            <!-- Location -->
            <div class="col-lg-6 col-md-6">
              <label class="form-label fw-semibold">
                <i class="fas fa-map-marker-alt me-1 text-primary"></i>
                Location *
              </label>
              <input
                v-model="form.location"
                type="text"
                class="form-control form-control-lg"
                :class="{ 'is-invalid': errors.location }"
                placeholder="City, State or ZIP"
                required
              />
              <div v-if="errors.location" class="invalid-feedback">
                {{ errors.location }}
              </div>
            </div>
          </div>

          <!-- Additional Options -->
          <div class="row g-3 mt-3">
            <div class="col-12">
              <div class="card bg-light border-0">
                <div class="card-body py-3">
                  <h6 class="card-title mb-3">
                    <i class="fas fa-cog me-2"></i>
                    Additional Options
                  </h6>
                  <div class="row g-3">
                    <div class="col-md-4">
                      <div class="form-check form-switch">
                        <input
                          v-model="form.multi_policy_discount"
                          class="form-check-input"
                          type="checkbox"
                          id="multiPolicy"
                        />
                        <label class="form-check-label" for="multiPolicy"> Multi-policy discount </label>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="form-check form-switch">
                        <input
                          v-model="form.safe_driver_discount"
                          class="form-check-input"
                          type="checkbox"
                          id="safeDriver"
                        />
                        <label class="form-check-label" for="safeDriver"> Safe driver discount </label>
                      </div>
                    </div>
                    <div class="col-md-4">
                      <div class="form-check form-switch">
                        <input v-model="form.loyalty_discount" class="form-check-input" type="checkbox" id="loyalty" />
                        <label class="form-check-label" for="loyalty"> Loyalty discount </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="row mt-4">
            <div class="col-12 text-center">
              <button type="submit" class="btn btn-primary btn-lg px-5 py-3" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-search me-2"></i>
                {{ loading ? 'Calculating...' : 'Get My Quote' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Results Section -->
    <div v-if="result" class="results-section mt-4">
      <div class="card shadow-sm border-0">
        <div class="card-header bg-success bg-gradient text-white">
          <h5 class="card-title mb-0">
            <i class="fas fa-check-circle me-2"></i>
            Your Insurance Quote
          </h5>
        </div>
        <div class="card-body p-4">
          <div class="row g-4">
            <!-- Quote Summary -->
            <div class="col-lg-8">
              <div class="quote-details">
                <div class="row g-3">
                  <div class="col-md-6">
                    <div class="detail-item">
                      <span class="detail-label">Policy Type:</span>
                      <span class="detail-value">{{ formatPolicyType(result.policy_type) }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="detail-item">
                      <span class="detail-label">Coverage Amount:</span>
                      <span class="detail-value">${{ formatCurrency(result.coverage) }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="detail-item">
                      <span class="detail-label">Location:</span>
                      <span class="detail-value">{{ result.location }}</span>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="detail-item">
                      <span class="detail-label">Age Group:</span>
                      <span class="detail-value">{{ result.age }} years</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Premium Display -->
            <div class="col-lg-4">
              <div class="premium-display text-center">
                <div class="premium-label">Your Premium</div>
                <div class="premium-amount">${{ formatCurrency(result.premium) }}</div>
                <div class="premium-period">per month</div>
                <button class="btn btn-outline-success mt-3">
                  <i class="fas fa-download me-2"></i>
                  Download Quote
                </button>
              </div>
            </div>
          </div>

          <!-- Discount Applied -->
          <div v-if="result.discounts_applied && result.discounts_applied.length > 0" class="mt-4">
            <div class="alert alert-info">
              <h6 class="alert-heading">
                <i class="fas fa-tag me-2"></i>
                Discounts Applied
              </h6>
              <ul class="mb-0">
                <li v-for="discount in result.discounts_applied" :key="discount">
                  {{ discount }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="alert alert-danger mt-4">
      <i class="fas fa-exclamation-triangle me-2"></i>
      {{ error }}
    </div>
  </div>
</template>

<script>
import api from '@/api/index'

export default {
  name: 'PremiumCalculator',
  data() {
    return {
      form: {
        policy_type: '',
        age: 30,
        coverage: 100000,
        location: '',
        risk_level: 'medium',
        multi_policy_discount: false,
        safe_driver_discount: false,
        loyalty_discount: false,
      },
      result: null,
      loading: false,
      error: null,
      errors: {},
    }
  },
  methods: {
    async onSubmit() {
      if (!this.validateForm()) return

      this.loading = true
      this.error = null

      try {
        const res = await api.post('/calculate-premium', this.form)
        this.result = res.data
        this.scrollToResults()
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to fetch quote. Please try again.'
      } finally {
        this.loading = false
      }
    },

    validateForm() {
      this.errors = {}
      let isValid = true

      if (!this.form.policy_type) {
        this.errors.policy_type = 'Please select a policy type'
        isValid = false
      }

      if (!this.form.age || this.form.age < 18 || this.form.age > 100) {
        this.errors.age = 'Please enter a valid age (18-100)'
        isValid = false
      }

      if (!this.form.coverage || this.form.coverage < 1000) {
        this.errors.coverage = 'Coverage amount must be at least $1,000'
        isValid = false
      }

      if (!this.form.location?.trim()) {
        this.errors.location = 'Please enter your location'
        isValid = false
      }

      return isValid
    },

    formatPolicyType(type) {
      const types = {
        auto: '🚗 Auto Insurance',
        home: '🏠 Home Insurance',
        life: '👤 Life Insurance',
        health: '🏥 Health Insurance',
      }
      return types[type] || type
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat('en-US').format(amount)
    },

    scrollToResults() {
      this.$nextTick(() => {
        const resultsElement = document.querySelector('.results-section')
        if (resultsElement) {
          resultsElement.scrollIntoView({ behavior: 'smooth' })
        }
      })
    },

    resetForm() {
      this.form = {
        policy_type: '',
        age: 30,
        coverage: 100000,
        location: '',
        risk_level: 'medium',
        multi_policy_discount: false,
        safe_driver_discount: false,
        loyalty_discount: false,
      }
      this.result = null
      this.errors = {}
    },
  },
}
</script>

<style scoped>
.premium-calculator {
  max-width: 1200px;
  margin: 0 auto;
}

.calculator-header {
  text-align: center;
  padding: 1rem 0;
}

.card {
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  border: none;
  padding: 1.5rem;
}

.form-control,
.form-select {
  border-radius: 8px;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.1);
}

.form-label {
  color: #495057;
  margin-bottom: 0.75rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.detail-label {
  font-weight: 500;
  color: #6c757d;
}

.detail-value {
  font-weight: 600;
  color: #212529;
}

.premium-display {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 2rem;
}

.premium-label {
  font-size: 0.9rem;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}

.premium-amount {
  font-size: 2.5rem;
  font-weight: 700;
  color: #198754;
  margin-bottom: 0.25rem;
}

.premium-period {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 1rem;
}

.btn-primary {
  border-radius: 8px;
  font-weight: 600;
  text-transform: none;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
}

.form-check-input:checked {
  background-color: #198754;
  border-color: #198754;
}

.alert {
  border-radius: 8px;
  border: none;
}

@media (max-width: 768px) {
  .premium-amount {
    font-size: 2rem;
  }

  .premium-display {
    padding: 1.5rem;
  }

  .card-body {
    padding: 2rem 1.5rem;
  }
}
</style>
