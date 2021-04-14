import { Link } from "react-router-dom"

function Home() {
  return (
    <div className="container pt-5">
      <div className="row mt-5" id="home-container">
        <div className="col" id="home-title-container">
          <div id="home-logo"></div>
          <h1>Loja da Música</h1>
        </div>

        <div className="col text-center d-flex align-items-center">
          <div>
            <p className="text-muted text-left pt-5" style={{ fontSize: "1.2rem" }}>
              Tem um show chegando e quer aparecer com aquele instrumento de alta qualidade, mas
              fica difícil de comprar um? Nós oferecemos instrumentos musicais e equipamentos
              relacionados para aluguel.
            </p>
            <Link
              to="/catalog"
              className="btn btn-outline-success mt-5 py-2 px-3"
              style={{ fontSize: "1.8rem", fontWeight: 600 }}
            >
              Veja nosso catálogo
            </Link>
          </div>
        </div>
      </div>

      <div className="row mt-5 pt-5">
        <div className="col d-flex justify-content-center align-items-center">
          <Link to="/register" className="btn btn-outline-primary" style={{ fontSize: "1.2rem" }}>
            Registre-se
          </Link>
          <span className="mx-4 text-muted" style={{ fontSize: "1.2rem" }}>
            ou
          </span>
          <Link to="/login" className="btn btn-outline-secondary" style={{ fontSize: "1.2rem" }}>
            Entre em sua conta
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Home
