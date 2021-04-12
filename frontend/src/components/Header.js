import { useContext } from "react"
import { Link } from "react-router-dom"
import userContext from "../context/UserContext"
import logo from "../assets/logo.png"

function Header() {
  const { userState } = useContext(userContext)

  return (
    <header className="bg-secondary text-light" style={{ height: "80px" }}>
      <div className="row container-fluid h-100 mx-auto px-5 align-items-center">
        <div className="col-md-1 h-100 d-flex align-items-center">
          <img src={logo} alt="Logo" style={{ height: "65%" }} />
        </div>
        <div className="col-md"></div>
        <div className="col-md-auto h-100 offset-md-7 d-flex">
          {userState ? <HeaderLoggedIn /> : <HeaderLoggedOut />}
        </div>
      </div>
    </header>
  )
}

function HeaderLoggedOut() {
  return (
    <div className="my-auto">
      <Link to="/login">
        <button className="btn btn-light">Entrar</button>
      </Link>
    </div>
  )
}

function HeaderLoggedIn() {
  const { userDispatch } = useContext(userContext)

  return (
    <div className="my-auto">
      <button className="btn btn-light" onClick={() => userDispatch({ type: "LOGOUT" })}>
        Sair
      </button>
    </div>
  )
}

export default Header
