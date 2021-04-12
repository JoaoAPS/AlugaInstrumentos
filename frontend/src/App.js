import { useReducer } from "react"
import { BrowserRouter, Switch, Route } from "react-router-dom"
// Components
import Login from "./pages/Login"
import Register from "./pages/Register"
import Header from "./components/Header"
// Context
import UserContext from "./context/UserContext"
import { userInitialState, userReducer } from "./context/userReducer"

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

            <Route path="/register">
              <Register />
            </Route>
          </Route>
        </Switch>
      </BrowserRouter>
    </UserContext.Provider>
  )
}

export default App
