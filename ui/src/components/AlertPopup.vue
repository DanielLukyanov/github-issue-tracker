<template>
    <div 
        v-if="condition"
        :class="['popup', { show: condition }, popupType]"
        @mouseenter="resetTimer"
        @mouseleave="startTimer"
    >
            <div class="close-btn" @click="closePopup">X</div>
            <h2>{{ popupName }}</h2>
            <p v-if="isError && errorCode" class="error-code">Error Code: {{ errorCode }}</p>
            <h3>{{ popupMessage }}</h3>
            <a
                v-if="issueUrl"
                :href="issueUrl"
                target="_blank"
                rel="noopener noreferrer"
            >
                {{ issueUrl }}
            </a>
            <div class="timer-bar" :style="{ width: `${timerWidth}%` }"></div>
     </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onUnmounted } from 'vue';


const props = defineProps<{
    popupName: string
    popupMessage: string
    issueUrl?: string
    condition: boolean
    type?: 'success' | 'error'
    errorCode?: string | number
}>()

const popupType = computed(() => props.type || 'success')
const isError = computed(() => popupType.value === 'error')

const emit = defineEmits<{
    (e: 'close'): void
}>()

const timerWidth = ref(100)
let timerInterval: number | null = null
let timerTimeout: number | null = null

const timer = ref(2)

function startTimer() {
    timerWidth.value = 100

    resetTimer()

    const totalMs = timer.value * 1000
    const intervalMs = 100
    const decrementPerTick = (intervalMs / totalMs) * 100

    timerTimeout = window.setTimeout(() => {
        closePopup()
    }, totalMs+150)

    timerInterval = window.setInterval(() => {
        timerWidth.value = Math.max(0, timerWidth.value - decrementPerTick)
    }, intervalMs)
}

function resetTimer() {
    timerWidth.value = 100
    timer.value = 2

    if (timerTimeout) {
        clearTimeout(timerTimeout)
        timerTimeout = null
    }
    if (timerInterval) {
        clearInterval(timerInterval)
        timerInterval = null
    }
}

function closePopup() {
    resetTimer()
    emit('close')
}

watch(
    () => props.condition,
    (newVal) => {
        if (newVal) {
            startTimer()
        } else {
            resetTimer()
        }
    },
    { immediate: true }
)

onUnmounted(() => {
    resetTimer()
})

</script>

<style scoped>
body {
    margin: 0;
}

.popup {
    position: fixed;
    top: 20px;
    left: 0;
    border-radius: 5px;
    padding: 15px;
    padding-right: 30px;
    box-shadow: 0 0px 10px rgba(0, 0, 0, 0.3);
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
    cursor: default;
}

.popup.success {
    background-color: #fff;
    color: #004e23;
    border-right: 4px solid #00a651;
}

.popup.success:hover {
    background-color: #effff7;
}

.popup.success .timer-bar {
    background-color: #003511;
}

.popup.error {
    background-color: #fff;
    color: #8b0000;
    border-right: 4px solid #d32f2f;
}

.popup.error:hover {
    background-color: #fff5f5;
}

.popup.error .timer-bar {
    background-color: #d32f2f;
}

.popup.show {
    transform: translateX(0);
}

.close-btn {
    position: absolute;
    top: 5px;
    right: 10px;
    cursor: pointer;
    font-weight: bold;
    color: #585858;
    cursor: pointer;
}

.timer-bar {
    height: 3px;
    transition: width 0.1s linear;
}

.error-code {
    font-size: 0.9em;
    font-weight: bold;
    margin: 5px 0;
    opacity: 0.8;
}

</style>