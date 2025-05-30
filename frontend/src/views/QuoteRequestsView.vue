<!-- QuoteRequestsView.vue -->

<template>
  <div>
    <h3>Quote Requests</h3>

    <div v-if="requests.length === 0" class="alert alert-info">No quote requests found.</div>

    <table v-else class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Policy</th>
          <th>Age</th>
          <th>Coverage</th>
          <th>Location</th>
          <th>When</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in requests" :key="r.id">
          <td>{{ r.id }}</td>
          <td>{{ r.policy_type }}</td>
          <td>{{ r.age }}</td>
          <td>{{ r.coverage }}</td>
          <td>{{ r.location }}</td>
          <td>{{ new Date(r.requested_at).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'QuoteRequestsView',
  data() {
    return {
      requests: [],
    }
  },
  async mounted() {
    try {
      const res = await api.get('/requests')
      this.requests = res.data
    } catch (err) {
      console.error(err)
      this.requests = []
    }
  },
}
</script>
