<template>
    <div 
        v-if="condition"
        :class="popupClasses"
        @mouseenter="pauseTimer"
        @mouseleave="resumeTimer"
    >
        <div class="close-btn" @click="closePopup">✕</div>
        <h2>{{ popupName }}</h2>
        <p v-show="errorCodeDisplay" class="error-code">{{ errorCodeDisplay }}</p>
        <h3>{{ popupMessage }}</h3>
        <a
            v-show="issueUrl"
            :href="issueUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="issue-link"
        >
            {{ issueUrl }}
        </a>
        <div class="timer-bar" :style="timerBarStyle"></div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onUnmounted } from 'vue'

const props = withDefaults(
    defineProps<{
        popupName: string
        popupMessage: string
        issueUrl?: string
        condition: boolean
        type?: 'success' | 'error'
        errorCode?: string | number
    }>(),
    {
        type: 'success'
    }
)

const emit = defineEmits<{
    (e: 'close'): void
}>()

// Constants
const TIMER_DURATION_MS = 2000
const TIMER_INTERVAL_MS = 100

// Reactive state
const timerWidth = ref(100)
let timerInterval: number | null = null
let timerTimeout: number | null = null

// Computed properties
const popupClasses = computed(() => ['popup', 'show', props.type])

const errorCodeDisplay = computed(() => 
    props.type === 'error' && props.errorCode 
        ? `Error Code: ${props.errorCode}` 
        : ''
)

const timerBarStyle = computed(() => ({
    width: `${timerWidth.value}%`
}))

// Timer management
function startTimer() {
    clearTimers()
    timerWidth.value = 100

    const decrementPerTick = (TIMER_INTERVAL_MS / TIMER_DURATION_MS) * 100

    timerInterval = window.setInterval(() => {
        timerWidth.value = Math.max(0, timerWidth.value - decrementPerTick)
        
        // Close popup when timer reaches 0, with buffer for animation
        if (timerWidth.value <= 0) {
            clearInterval(timerInterval!)
            timerInterval = null
            timerTimeout = window.setTimeout(() => {
                closePopup()
            }, 150)
        }
    }, TIMER_INTERVAL_MS)
}

function clearTimers() {
    if (timerTimeout) {
        clearTimeout(timerTimeout)
        timerTimeout = null
    }
    if (timerInterval) {
        clearInterval(timerInterval)
        timerInterval = null
    }
}

function pauseTimer() {
    clearTimers()
}

function resumeTimer() {
    if (props.condition && timerWidth.value > 0) {
        const decrementPerTick = (TIMER_INTERVAL_MS / TIMER_DURATION_MS) * 100

        timerInterval = window.setInterval(() => {
            timerWidth.value = Math.max(0, timerWidth.value - decrementPerTick)
            
            // Close popup when timer reaches 0, with buffer for animation
            if (timerWidth.value <= 0) {
                clearInterval(timerInterval!)
                timerInterval = null
                timerTimeout = window.setTimeout(() => {
                    closePopup()
                }, 150)
            }
        }, TIMER_INTERVAL_MS)
    }
}

function closePopup() {
    clearTimers()
    timerWidth.value = 100
    emit('close')
}

// Watchers
watch(
    () => props.condition,
    (isVisible) => {
        if (isVisible) {
            startTimer()
        } else {
            clearTimers()
            timerWidth.value = 100
        }
    },
    { immediate: true }
)

onUnmounted(() => {
    clearTimers()
})

</script>

<style scoped>
.popup {
    position: fixed;
    top: 20px;
    left: 0;
    padding: 15px 30px 15px 15px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
    cursor: default;
    background-color: #fff;
    min-width: 400px;
}

.popup.show {
    transform: translateX(0);
}

/* Success variant */
.popup.success {
    color: #004e23;
    border-right: 4px solid #00a651;
}

.popup.success:hover {
    background-color: #effff7;
}

.popup.success .timer-bar {
    background-color: #003511;
}

/* Error variant */
.popup.error {
    color: #8b0000;
    border-right: 4px solid #d32f2f;
}

.popup.error:hover {
    background-color: #fff5f5;
}

.popup.error .timer-bar {
    background-color: #d32f2f;
}

/* Elements */
.close-btn {
    position: absolute;
    top: 5px;
    right: 10px;
    font-weight: bold;
    font-size: 18px;
    color: #585858;
    cursor: pointer;
    user-select: none;
}

.close-btn:hover {
    color: #000;
}

.error-code {
    font-size: 0.9em;
    font-weight: bold;
    margin: 5px 0;
    opacity: 0.8;
}

.issue-link {
    display: inline-block;
    margin-top: 8px;
    word-break: break-all;
}

.timer-bar {
    height: 3px;
    margin-top: 10px;
    transition: width 0.1s linear;
}
</style>