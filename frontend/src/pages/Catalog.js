import CatalogSidebar from "../components/CatalogSidebar"
import tmp_fig from "../assets/logo.png"
import CatalogItem from "../components/CatalogItem"

function Catalog() {
  const tmp_items = [
    { id: 0, title: "Lorem Ipsum", image: tmp_fig, price: 10 },
    { id: 1, title: "Lorem Ipsum", image: tmp_fig, price: 20.1 },
    { id: 2, title: "Lorem Ipsum", image: tmp_fig, price: 12.5 },
    { id: 3, title: "Lorem Ipsum", image: tmp_fig, price: 40.77 },
    { id: 4, title: "Lorem Ipsum", image: tmp_fig, price: 2 },
    { id: 5, title: "Lorem Ipsum", image: tmp_fig, price: 4.947 },
    { id: 6, title: "Lorem Ipsum", image: tmp_fig, price: 5.89 },
  ]

  return (
    <div className="container-lg px-5 px-lg-0">
      <h1>Catálogo</h1>

      <div className="row">
        <div className="col-lg-3 col-md-3">
          <CatalogSidebar />
        </div>

        <div className="col">
          <div className="row row-cols-md-3 row-cols-lg-4">
            {tmp_items.map((item, idx) => (
              <CatalogItem key={item.id} {...item} idx={idx} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Catalog
