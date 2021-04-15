import { useEffect, useReducer } from "react"
import api, { CancelToken } from "../API"
import CatalogSidebar from "../components/CatalogSidebar"
import CatalogItem from "../components/CatalogItem"

const reducer = (prev, action) => {
  const { type, payload } = action

  if (type === "UPDATE_FILTERS") {
    console.log(payload)
    let new_url = "equipamentos?"
    if (payload.isInstrument !== null) {
      new_url += "&instrumento=" + (payload.isInstrument ? "1" : "0")
    }
    if (payload.categoria !== null) {
      new_url += `&categorias=${payload.categoria}`
    }

    return {
      ...prev,
      isInstrument: payload.isInstrument,
      categoria: payload.categoria,
      fetch_url: new_url,
    }
  }

  if (type === "CLEAR_FILTERS") {
    return {
      ...prev,
      isInstrument: null,
      categoria: null,
      fetch_url: "equipamentos",
    }
  }

  if (type === "SET_DATA") {
    return { ...prev, items: payload, isLoading: false, error: false }
  }

  if (type === "SET_ERROR") {
    return { ...prev, isLoading: false, error: payload }
  }

  return prev
}

function Catalog() {
  const [state, dispatch] = useReducer(reducer, {
    isInstrument: null,
    categoria: null,
    items: [],
    isLoading: true,
    error: null,
    fetch_url: "equipamentos",
  })

  useEffect(() => {
    const cancelSource = CancelToken.source()

    api
      .get(state.fetch_url, { cancelToken: cancelSource.token })
      .then(res => {
        dispatch({ type: "SET_DATA", payload: res.data })
      })
      .catch(err => {
        dispatch({
          type: "SET_ERROR",
          payload: err.response
            ? err.response.status + " - " + err.response.statusText
            : "Houve um erro na requisição de dados!",
        })
      })

    return () => cancelSource.cancel()
  }, [state.fetch_url])

  if (state.error) return <h3>Erro: {state.error}</h3>
  if (state.items === null) return <h3>Item null</h3>

  return (
    <div className="container-lg px-5 px-lg-0">
      <h1>Catálogo</h1>

      <div className="row">
        <div className="col-lg-3 col-md-3">
          <CatalogSidebar dispatch={dispatch} activeCat={state.categoria} />
        </div>

        <div className="col">
          {state.isLoading ? (
            <h3>Loading...</h3>
          ) : state.items.length > 0 ? (
            <div className="row row-cols-md-3 row-cols-lg-4">
              {state.items.map((item, idx) => (
                <CatalogItem key={item.id} {...item} idx={idx} />
              ))}
            </div>
          ) : (
            <p style={{ fontSize: "1.5rem" }} className="p-4">
              Ops, parece que não há nenhum item no momento.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Catalog
