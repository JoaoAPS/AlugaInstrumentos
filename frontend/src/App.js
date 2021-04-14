import { useReducer } from "react"
import { BrowserRouter, Switch, Route, Redirect } from "react-router-dom"
// Context
import UserContext from "./context/UserContext"
import { userInitialState, userReducer } from "./context/userReducer"
import Home from "./pages/Home"
// Components
import Login from "./pages/Login"
import Register from "./pages/Register"
import Header from "./components/Header"
import Catalog from "./pages/Catalog"

function App() {
  const [userState, userDispatch] = useReducer(userReducer, userInitialState)

  return (
    <UserContext.Provider value={{ userState, userDispatch }}>
      <BrowserRouter>
        <Switch>
          <Route path="/login">
            <Login />
          </Route>

          <Route path="/">
            <Header />

            <Route path="/" exact>
              <Redirect to="/home" />
            </Route>

            <Route path="/home">
              <Home />
            </Route>

            <Route path="/register">
              <Register />
            </Route>

            <Route path="/catalog">
              <Catalog />
            </Route>
          </Route>
        </Switch>
      </BrowserRouter>
    </UserContext.Provider>
  )
}

export default App
