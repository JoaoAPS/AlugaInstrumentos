import { useState, useEffect, useContext, useCallback } from "react"
import { Link, useHistory } from "react-router-dom"
import { usePrevious } from "../hooks/usePrevious"
import api, { CancelToken } from "../API"
import UserContext from "../context/UserContext"

function Register() {
  const [email, setEmail] = useState({ value: "", error: "" })
  const [name, setName] = useState({ value: "", error: "" })
  const [password1, setPassword1] = useState({ value: "", error: "" })
  const [password2, setPassword2] = useState({ value: "", error: "" })
  const [submitCount, setSubmitCount] = useState(0)
  const prevSubmitCount = usePrevious(submitCount)
  const { userDispatch } = useContext(UserContext)
  const history = useHistory()

  const validateEmail = useCallback(() => {
    if (!email.value || !/.+@.+/.test(email.value)) {
      setEmail({ ...email, error: "Email inválido." })
      return false
    }
    return true
  }, [email])

  const validateName = useCallback(() => {
    if (!name.value) {
      setName({ ...name, error: "Insira seu nome." })
      return false
    }
    return true
  }, [name])

  const validatePassword1 = useCallback(() => {
    if (!password1.value) {
      setPassword1({ ...password1, error: "Insira uma senha." })
      return false
    }

    if (password1.value.length < 6) {
      setPassword1({ ...password1, error: "Senha muito curta." })
      return false
    }

    return true
  }, [password1])

  const validatePassword2 = useCallback(() => {
    if (password1.value !== password2.value) {
      setPassword2({ ...password2, error: "As duas senhas devem ser iguais." })
      return false
    }
    return true
  }, [password1, password2])

  const handleSubmit = e => {
    e.preventDefault()
    setSubmitCount(prev => prev + 1)
  }

  // Submit registration
  useEffect(() => {
    if (submitCount === 0) return
    if (submitCount === prevSubmitCount) return
    console.log("Submitting")

    const isEmailValid = validateEmail()
    const isNameValid = validateName()
    const isPassword1Valid = validatePassword1()
    const isPassword2Valid = validatePassword2()

    if (!isEmailValid || !isNameValid || !isPassword1Valid || !isPassword2Valid) return

    const cancelSource = CancelToken.source()
    api
      .post(
        "registration/register/",
        {
          email: email.value,
          name: name.value,
          password1: password1.value,
          password2: password2.value,
        },
        { cancelToken: cancelSource.token }
      )
      .then(res => {
        userDispatch({ type: "LOGIN", payload: res.data })
        history.push("/")
      })
      .catch(err => {
        if (err.response.data.email) setEmail({ ...email, error: "Email inválido." })
        if (err.response.data.name) setName({ ...name, error: "Nome inválido." })
        if (err.response.data.password1)
          setPassword1({ ...password1, error: err.response.password1 })
        if (err.response.data.password2)
          setPassword2({ ...password2, error: err.response.password2 })
      })

    return () => cancelSource.cancel()
  }, [
    submitCount,
    prevSubmitCount,
    email,
    name,
    password1,
    password2,
    validateEmail,
    validateName,
    validatePassword1,
    validatePassword2,
    history,
    userDispatch,
  ])

  return (
    <div className="container" style={{ maxWidth: "700px" }}>
      <h2 className="mt-5 mb-1">Registre-se na Loja de Música</h2>

      <small className="text-muted">Já tem uma conta?</small>
      <Link to="/login">
        <small className="text-info px-2">Entre aqui</small>
      </Link>

      <form className="mt-5" onSubmit={handleSubmit}>
        <FormField
          name="email"
          object={email}
          setter={setEmail}
          label="Email"
          placeholder="Digite seu endereço de email"
          validate={validateEmail}
        />

        <FormField
          name="name"
          object={name}
          setter={setName}
          label="Nome"
          placeholder="Digite seu nome completo"
          validate={validateName}
        />

        <FormField
          name="password1"
          object={password1}
          type="password"
          setter={setPassword1}
          label="Senha"
          placeholder="Digite sua senha"
          validate={validatePassword1}
        />

        <FormField
          name="password2"
          object={password2}
          type="password"
          setter={setPassword2}
          label="Confirme sua senha"
          placeholder="Digite sua senha novamente"
          validate={validatePassword2}
        />

        <div className="text-center mt-5">
          <button className="btn btn-primary">Registrar</button>
        </div>
      </form>
    </div>
  )
}

function FormField({ name, object, setter, label, type, placeholder, validate }) {
  return (
    <div className="form-group">
      <label htmlFor={`${name}-field`}>{label}</label>
      <input
        id={`${name}-field`}
        type={type || "text"}
        placeholder={placeholder || ""}
        className={"form-control " + (object.error && "is-invalid")}
        value={object.value}
        onChange={e => setter({ error: "", value: e.target.value })}
        onBlur={validate}
      />
      {object.error && <small className="invalid-feedback">{object.error}</small>}
    </div>
  )
}

export default Register
