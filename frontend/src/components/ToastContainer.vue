<template>
  <div class="toast-container" aria-live="polite" aria-atomic="false">
    <transition-group name="toast">
      <div
        v-for="t in toastState.items"
        :key="t.id"
        :class="['toast', `toast-${t.type}`]"
        :role="t.type === 'confirm' ? 'alertdialog' : 'alert'"
      >
        <span class="toast-icon" aria-hidden="true">
          <svg v-if="t.type === 'success'" viewBox="0 0 20 20" fill="none">
            <path d="M5 10.5 8.5 14 15 6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <svg v-else-if="t.type === 'error'" viewBox="0 0 20 20" fill="none">
            <path d="M6 6l8 8M14 6l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
          <svg v-else viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="6" r="1.2" fill="currentColor" />
            <path d="M10 9.5V14.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </span>

        <div class="toast-body">
          <p class="toast-message">{{ t.message }}</p>
          <div v-if="t.type === 'confirm'" class="toast-actions">
            <button type="button" class="toast-btn confirm" @click="respond(t, true)">{{ t.confirmText }}</button>
            <button type="button" class="toast-btn cancel" @click="respond(t, false)">{{ t.cancelText }}</button>
          </div>
        </div>

        <button
          v-if="t.type !== 'confirm'"
          type="button"
          class="toast-close"
          aria-label="Dismiss notification"
          @click="dismiss(t.id)"
        >
          &times;
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { toastState, toast } from '../composables/toast'

export default {
  name: 'ToastContainer',
  setup() {
    const dismiss = (id) => toast.dismiss(id)
    const respond = (t, value) => {
      if (t.resolve) t.resolve(value)
      toast.dismiss(t.id)
    }
    return { toastState, dismiss, respond }
  },
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1.25rem;
  right: 1.25rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 360px;
  max-width: calc(100vw - 2rem);
  pointer-events: none;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.toast {
  pointer-events: auto;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.9rem 1rem;
  border-radius: 10px;
  background: #ffffff;
  color: #2d3748;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border: 1px solid #edf2f7;
  border-left: 4px solid #a0aec0;
}

.toast-success { border-left-color: #38a169; }
.toast-error { border-left-color: #e53e3e; }
.toast-info { border-left-color: #3182ce; }
.toast-confirm { border-left-color: #dd6b20; }

.toast-icon {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1px;
}

.toast-icon svg {
  width: 14px;
  height: 14px;
}

.toast-success .toast-icon { background: #c6f6d5; color: #276749; }
.toast-error .toast-icon { background: #fed7d7; color: #c53030; }
.toast-info .toast-icon { background: #ebf8ff; color: #2b6cb0; }
.toast-confirm .toast-icon { background: #feebc8; color: #c05621; }

.toast-body {
  flex: 1;
  min-width: 0;
}

.toast-message {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
  font-weight: 500;
  word-break: break-word;
}

.toast-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.toast-btn {
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  border: none;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.toast-btn.confirm {
  background: #3182ce;
  color: #fff;
}
.toast-btn.confirm:hover { background: #2b6cb0; }

.toast-btn.cancel {
  background: #edf2f7;
  color: #4a5568;
}
.toast-btn.cancel:hover { background: #e2e8f0; }

.toast-close {
  flex-shrink: 0;
  background: none;
  border: none;
  color: #a0aec0;
  font-size: 1.2rem;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}
.toast-close:hover { color: #4a5568; }

.toast-enter-active,
.toast-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.toast-enter-from {
  transform: translateX(120%);
  opacity: 0;
}
.toast-leave-to {
  transform: translateX(120%);
  opacity: 0;
}
.toast-leave-active {
  position: absolute;
  right: 0;
  width: 100%;
}

@media (max-width: 480px) {
  .toast-container {
    left: 1rem;
    right: 1rem;
    width: auto;
  }
}
</style>
