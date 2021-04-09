export const userInitialState = null

export function userReducer(prev, action) {
  const { type, payload } = action

  if (type === "LOGIN") {
    localStorage.setItem("lojaMusicaToken", payload.token)
    return payload.user
  }
}
