export const userInitialState = null

export function userReducer(prev, action) {
  const { type, payload } = action

  if (type === "LOGIN") {
    localStorage.setItem("lojaMusicaToken", payload.token)
    return {
      id: payload.id,
      email: payload.email,
      name: payload.name,
    }
  }

  if (type === "LOGOUT") {
    localStorage.removeItem("lojaMusicaToken")
    return null
  }
}
