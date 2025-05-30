<template>
  <div>
    <h3>Past Requests</h3>
    <table class="table">
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
  name: 'HistoryView',
  data() {
    return { requests: [] }
  },
  async mounted() {
    const res = await api.get('/requests')
    this.requests = res.data
  },
}
</script>
