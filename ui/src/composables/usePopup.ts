import { ref, computed } from 'vue'

interface PopupState {
    visible: boolean
    type: 'success' | 'error'
    name: string
    message: string
    issueUrl: string
    errorCode: string | number
}

const popup = ref<PopupState>({
    visible: false,
    type: 'success',
    name: '',
    message: '',
    issueUrl: '',
    errorCode: ''
})

export function usePopup() {
    function showPopup(options: {
        type: 'success' | 'error'
        message: string
        name?: string
        issueUrl?: string
        errorCode?: string | number
    }) {
        popup.value = {
            visible: true,
            type: options.type,
            name: options.name || (options.type === 'success' ? 'Success' : 'Error'),
            message: options.message,
            issueUrl: options.issueUrl || '',
            errorCode: options.errorCode || ''
        }
    }

    function closePopup() {
        popup.value.visible = false
    }

    return {
        popup: computed(() => popup.value),
        showPopup,
        closePopup
    }
}
