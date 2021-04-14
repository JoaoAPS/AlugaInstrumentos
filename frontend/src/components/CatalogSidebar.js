function CatalogSidebar() {
  const instruments = ["Sopro", "Violão", "Guitarra", "Bateria"]
  const equipaments = ["Caixas de som", "Cabos", "Pedais"]

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
        <h5>Instrumentos</h5>

        <ul className="list-unstyled m-0">
          {instruments.map(instr => (
            <li key={instr} className="text-capitalize pl-4 pt-2">
              {instr}
            </li>
          ))}
        </ul>
      </CatalogSidebarSection>

      <CatalogSidebarSection key="equipaments">
        <h5>Equipamentos</h5>

        <ul className="list-unstyled m-0">
          {equipaments.map(equip => (
            <li key={equip} className="text-capitalize pl-4 pt-2">
              {equip}
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
