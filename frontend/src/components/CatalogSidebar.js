import useFetch from "../hooks/useFetch"

function CatalogSidebar({ dispatch }) {
  const { data: categorias, isLoading, error } = useFetch("categorias")

  if (isLoading) return <div></div>
  if (error) return <h3>Erro ao carregar categorias!</h3>
  if (categorias === null) return <h3>Null</h3>

  return (
    <>
      <CatalogSidebarSection key="dates" className="text-center">
        <span className="text-muted">Início do aluguel</span>
        <br />
        <SidebarDateinput value="21/06/2021" />
        <br />
        <br />

        <span className="text-muted">Término do aluguel</span>
        <SidebarDateinput value="24/06/2021" />
      </CatalogSidebarSection>

      <CatalogSidebarSection key="instruments">
        <h5
          style={{ cursor: "pointer" }}
          onClick={() =>
            dispatch({
              type: "FILTER_INSTRUMENT",
              payload: { isIstrument: true, categoria: null },
            })
          }
        >
          Instrumentos
        </h5>

        <ul className="list-unstyled m-0">
          {categorias
            .filter(cat => cat.is_instrument)
            .map(instr => (
              <li
                key={instr.id}
                className="text-capitalize pl-4 pt-2"
                style={{ cursor: "pointer" }}
                onClick={() =>
                  dispatch({
                    type: "FILTER_INSTRUMENT",
                    payload: { isIstrument: true, categoria: instr.id },
                  })
                }
              >
                {instr.name}
              </li>
            ))}
        </ul>
      </CatalogSidebarSection>

      <CatalogSidebarSection key="equipaments">
        <h5
          style={{ cursor: "pointer" }}
          onClick={() =>
            dispatch({
              type: "FILTER_INSTRUMENT",
              payload: { isIstrument: false, categoria: null },
            })
          }
        >
          Equipamentos
        </h5>

        <ul className="list-unstyled m-0">
          {categorias
            .filter(cat => !cat.is_instrument)
            .map(equip => (
              <li
                key={equip.id}
                style={{ cursor: "pointer" }}
                className="text-capitalize pl-4 pt-2"
                onClick={() =>
                  dispatch({
                    type: "FILTER_INSTRUMENT",
                    payload: { isIstrument: false, categoria: equip.id },
                  })
                }
              >
                {equip.name}
              </li>
            ))}
        </ul>
      </CatalogSidebarSection>
    </>
  )
}

function CatalogSidebarSection(props) {
  const styles = {
    borderBottom: props.hideSeparator ? "none" : "solid 1px #666",
    paddingBottom: "30px",
    marginBottom: "20px",
    ...props.styles,
  }

  return (
    <section style={styles} className={props.className}>
      {props.children}
    </section>
  )
}

function SidebarDateinput({ value }) {
  return (
    <input
      type="text"
      className="text-center py-1 mx-auto"
      style={{ border: "none", borderBottom: "solid 1px #aaa", width: "80%" }}
      value={value}
    />
  )
}

export default CatalogSidebar
