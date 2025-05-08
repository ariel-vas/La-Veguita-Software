// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  css: ['@/assets/css/tailwind.css'],
  modules: ['@nuxtjs/tailwindcss'],
  app: {
    head: {
      title: 'La Veguita',  
      link: [
        { rel: 'icon', href: '/laveguitalogo-removebg-preview.png' }  
      ]
    }
  }
})
