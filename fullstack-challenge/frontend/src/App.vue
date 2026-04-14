<template>
  <main class="container">
    <h1>Directorio de Proveedores Inteligente</h1>

    <section class="card">
      <h2>{{ editId ? 'Editar proveedor' : 'Nuevo proveedor' }}</h2>
      <form @submit.prevent="submitProvider">
        <div class="grid">
          <input v-model="form.name" placeholder="Nombre" required />
          <input v-model="form.service_type" placeholder="Tipo de servicio" required />
          <input v-model="form.email" type="email" placeholder="Email" required />
          <input v-model="form.phone" placeholder="Teléfono" />
          <input v-model="form.city" placeholder="Ciudad" />
        </div>
        <textarea v-model="form.description" placeholder="Descripción del proveedor" required />
        <div class="actions">
          <button type="submit">{{ editId ? 'Actualizar' : 'Guardar' }}</button>
          <button v-if="editId" type="button" @click="resetForm" class="ghost">Cancelar</button>
        </div>
      </form>
    </section>

    <section class="card">
      <h2>Buscar proveedores</h2>
      <input v-model="query" @input="loadProviders" placeholder="Busca por texto, ciudad o categoría IA" />

      <p v-if="loading">Cargando...</p>
      <p v-if="error" class="error">{{ error }}</p>

      <table v-if="providers.length">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Servicio</th>
            <th>Ciudad</th>
            <th>Categoría IA</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in providers" :key="p.id">
            <td>{{ p.name }}</td>
            <td>{{ p.service_type }}</td>
            <td>{{ p.city || 'N/A' }}</td>
            <td><span class="pill">{{ p.ai_category || 'General' }}</span></td>
            <td>
              <button @click="startEdit(p)">Editar</button>
              <button class="danger" @click="removeProvider(p.id)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No hay proveedores registrados.</p>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { createProvider, deleteProvider, fetchProviders, updateProvider } from './services/api'

const providers = ref([])
const query = ref('')
const loading = ref(false)
const error = ref('')
const editId = ref(null)

const form = reactive({
  name: '',
  service_type: '',
  description: '',
  email: '',
  phone: '',
  city: ''
})

const resetForm = () => {
  editId.value = null
  Object.assign(form, {
    name: '',
    service_type: '',
    description: '',
    email: '',
    phone: '',
    city: ''
  })
}

const loadProviders = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await fetchProviders(query.value)
    providers.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || 'No se pudieron cargar proveedores'
  } finally {
    loading.value = false
  }
}

const submitProvider = async () => {
  error.value = ''
  try {
    if (editId.value) {
      await updateProvider(editId.value, form)
    } else {
      await createProvider(form)
    }
    resetForm()
    await loadProviders()
  } catch (err) {
    error.value = err.response?.data?.detail || 'No se pudo guardar'
  }
}

const startEdit = (provider) => {
  editId.value = provider.id
  Object.assign(form, {
    name: provider.name,
    service_type: provider.service_type,
    description: provider.description,
    email: provider.email,
    phone: provider.phone || '',
    city: provider.city || ''
  })
}

const removeProvider = async (id) => {
  if (!confirm('¿Eliminar proveedor?')) return
  await deleteProvider(id)
  await loadProviders()
}

onMounted(loadProviders)
</script>
