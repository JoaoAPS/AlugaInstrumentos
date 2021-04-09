import axios from "axios"

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
})

export const CancelToken = axios.CancelToken

// class API {
//   constructor() {
//     this.axios_instance = axios.create({
//       baseURL: "http://localhost:8000/api/",
//     })
//   }

//   get(url, ...args) {
//     this.axios_instance.get(url, ...args)
//   }

//   post(url, ...args) {
//     this.axios_instance.post(url, ...args)
//   }

//   put(url, ...args) {
//     this.axios_instance.put(url, ...args)
//   }

//   patch(url, ...args) {
//     this.axios_instance.patch(url, ...args)
//   }

//   delete(url, ...args) {
//     this.axios_instance.delete(url, ...args)
//   }
// }

export default api
