import { useEffect, useReducer } from "react"
import api, { CancelToken } from "../API"
import CatalogSidebar from "../components/CatalogSidebar"
import CatalogItem from "../components/CatalogItem"

const reducer = (prev, action) => {
  const { type, payload } = action

  if (type === "UPDATE_FILTER") {
    return {
      ...prev,
      isInstrument: payload.isInstrument,
      categoria: payload.categoria,
      fetchCount: prev.fetchCount + 1,
      isLoading: true,
    }
  }

  if (type === "SET_DATA") {
    return { ...prev, items: payload, isLoading: false, error: false }
  }

  if (type === "SET_ERROR") {
    return { ...prev, isLoading: false, error: payload }
  }
}

function Catalog() {
  const [state, dispatch] = useReducer(reducer, {
    fetchCount: 0,
    isInstrument: null,
    categoria: null,
    items: [],
    isLoading: true,
    error: null,
  })

  useEffect(() => {
    const cancelSource = CancelToken.source()

    api
      .get("equipamentos", { cancelToken: cancelSource.token })
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
  }, [state.fetchCount])

  if (state.isLoading) return <h3>Loading...</h3>
  if (state.error) return <h3>Erro: {state.error}</h3>
  if (state.items === null) return <h3>Item null</h3>

  return (
    <div className="container-lg px-5 px-lg-0">
      <h1>Catálogo</h1>

      <div className="row">
        <div className="col-lg-3 col-md-3">
          <CatalogSidebar dispatch={dispatch} />
        </div>

        <div className="col">
          <div className="row row-cols-md-3 row-cols-lg-4">
            {state.items.map((item, idx) => (
              <CatalogItem key={item.id} {...item} idx={idx} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Catalog
