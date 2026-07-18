import { reactive } from 'vue'

let nextId = 0

// Reactive singleton store shared across the whole app.
// Rendered once by <ToastContainer /> mounted in App.vue.
export const toastState = reactive({
  items: [],
})

function remove(id) {
  const index = toastState.items.findIndex((t) => t.id === id)
  if (index === -1) return
  const [item] = toastState.items.splice(index, 1)
  if (item && item.timer) clearTimeout(item.timer)
}

function push(item) {
  const id = ++nextId
  const entry = { id, ...item }
  toastState.items.push(entry)
  if (entry.duration > 0) {
    entry.timer = setTimeout(() => remove(id), entry.duration)
  }
  return id
}

export const toast = {
  show(message, type = 'info', duration = 4000) {
    return push({ message, type, duration })
  },
  success(message, duration = 4000) {
    return push({ message, type: 'success', duration })
  },
  error(message, duration = 5000) {
    return push({ message, type: 'error', duration })
  },
  info(message, duration = 4000) {
    return push({ message, type: 'info', duration })
  },
  dismiss(id) {
    remove(id)
  },
  // Confirmation toast: returns a Promise that resolves to true when the user
  // confirms and false when they cancel. Never auto-dismisses.
  confirm(message, { confirmText = 'Confirm', cancelText = 'Cancel' } = {}) {
    return new Promise((resolve) => {
      push({ message, type: 'confirm', duration: 0, confirmText, cancelText, resolve })
    })
  },
}

// Vue plugin: exposes `this.$toast` in every component.
export const ToastPlugin = {
  install(app) {
    app.config.globalProperties.$toast = toast
  },
}

export default toast
