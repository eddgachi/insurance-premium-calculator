<!-- QuoteResultsView.vue -->

<template>
  <div>
    <h3>Quote Results</h3>

    <div v-if="results.length === 0" class="alert alert-info">No quote results available.</div>

    <table v-else class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Request ID</th>
          <th>Premium</th>
          <th>Fetched At</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in results" :key="r.id">
          <td>{{ r.id }}</td>
          <td>{{ r.request_id }}</td>
          <td>{{ r.premium }}</td>
          <td>{{ new Date(r.fetched_at).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'QuoteResultsView',
  data() {
    return {
      results: [],
    }
  },
  async mounted() {
    try {
      const res = await api.get('/results')
      this.results = res.data
    } catch (err) {
      console.error(err)
      this.results = []
    }
  },
}
</script>
