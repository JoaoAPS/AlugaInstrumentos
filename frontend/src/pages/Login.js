import { useState, useContext, useEffect } from "react"
import { Link } from "react-router-dom"
import userContext from "../context/UserContext"
import api, { CancelToken } from "../API"

function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [submitCount, setSubmitCount] = useState(0)
  const [error, setError] = useState("")
  const { userDispatch } = useContext(userContext)

  function handleSubmit(e) {
    e.preventDefault()
    setSubmitCount(prev => prev + 1)
  }

  useEffect(() => {
    if (submitCount == 0) return

    const cancelSource = CancelToken.source()

    api
      .post("/login/", { username: email, password: password }, { cancelToken: cancelSource.token })
      .then(res => {
        userDispatch({ type: "LOGIN", payload: res.data })
      })
      .catch(err => {
        const error_msg = err.response.data.non_field_errors
          ? err.response.data.non_field_errors[0]
          : false

        if (error_msg) {
          setError(
            error_msg === "Unable to log in with provided credentials."
              ? "Email ou senha inválido!"
              : err.msg
          )
        } else {
          setError("Houve um erro ao tentar entrar.")
        }
      })

    return () => cancelSource.cancel()
  }, [submitCount])

  useEffect(() => {
    setError("")
  }, [email, password])

  return (
    <div id="login-container" className="container pb-5" style={{ maxWidth: "900px" }}>
      <div className="row pt-5">
        <Link to="/">
          <small className="text-muted">&larr; Continuar navegando sem entrar</small>
        </Link>
      </div>

      <div className="row mt-3">
        <div className="col-md-3" />
        <div className="col-md-6">
          <div className="row my-5">
            <div className="text-center col-md-12">
              <h2>Entre em sua conta</h2>
            </div>
          </div>

          <div className="row">
            <div className="col-md-12">
              {error != "" && <small className="text-danger">{error}</small>}

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label for="email-field">Email</label>
                  <input
                    id="email-field"
                    type="email"
                    className="form-control"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                  />
                </div>

                <div className="form-group">
                  <label for="password-field">Senha</label>
                  <input
                    id="password-field"
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                  />
                </div>

                <div className="row text-center pt-3">
                  <button type="submit" className="btn btn-primary mx-auto px-4">
                    Entrar
                  </button>
                </div>
              </form>
            </div>
          </div>

          <div className="row text-center mt-5">
            <div className="col">
              <span>Ainda não tem uma conta?</span>
              <Link to="/register" className="text-info px-1">
                Registre-se aqui
              </Link>
            </div>
          </div>
        </div>
        <div className="col-md-3" />
      </div>
    </div>
  )
}

export default Login
