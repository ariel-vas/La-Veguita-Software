import { ref } from 'vue'

const activePage = ref<string>('')

export const useActivePage = () => {
  const setActivePage = (page: string | undefined) => {
    if (!page) return
    activePage.value = page
  }

  return {
    activePage,
    setActivePage
  }
}
