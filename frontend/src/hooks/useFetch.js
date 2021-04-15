import { useEffect, useState } from "react"
import api, { CancelToken } from "../API"

const useFetch = url => {
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)

  useEffect(() => {
    const cancelSource = CancelToken.source()

    api
      .get(url, { cancelToken: cancelSource.token })
      .then(res => {
        setData(res.data)
      })
      .catch(err => {
        setError(
          err.response
            ? err.response.status + " - " + err.response.statusText
            : "Houve um erro na requisição de dados!"
        )
      })

    setIsLoading(false)

    return () => cancelSource.cancel()
  }, [url])

  return { data, isLoading, error }
}

export default useFetch
