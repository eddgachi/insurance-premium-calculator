<!-- components/PremiumCalculator.vue -->

<template>
  <div class="card p-4">
    <h3>Calculate Premium</h3>
    <form @submit.prevent="onSubmit" class="row g-3">
      <div class="col-md-3">
        <label class="form-label">Policy Type</label>
        <select v-model="form.policy_type" class="form-select" required>
          <option value="auto">Auto</option>
          <option value="home">Home</option>
          <option value="life">Life</option>
        </select>
      </div>
      <div class="col-md-2">
        <label class="form-label">Age</label>
        <input v-model.number="form.age" type="number" min="18" class="form-control" required />
      </div>
      <div class="col-md-3">
        <label class="form-label">Coverage Amount</label>
        <input v-model.number="form.coverage" type="number" min="1" class="form-control" required />
      </div>
      <div class="col-md-4">
        <label class="form-label">Location</label>
        <input v-model="form.location" type="text" class="form-control" required />
      </div>
      <div class="col-12">
        <button class="btn btn-primary">Get Quote</button>
      </div>
    </form>

    <div v-if="result" class="mt-4">
      <h5>Your Quote</h5>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Policy</th>
            <th>Coverage</th>
            <th>Premium</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ result.policy_type }}</td>
            <td>{{ result.coverage }}</td>
            <td>{{ result.premium }}</td>
          </tr>
        </tbody>
      </table>
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
        policy_type: 'auto',
        age: 30,
        coverage: 100000,
        location: '',
      },
      result: null,
    }
  },
  methods: {
    async onSubmit() {
      try {
        const res = await api.post('/calculate-premium', this.form)
        this.result = res.data
      } catch (err) {
        alert(err.response?.data?.detail || 'Failed to fetch quote')
      }
    },
  },
}
</script>
