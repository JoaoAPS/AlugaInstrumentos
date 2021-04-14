function CatalogItem({ title, price, image, idx }) {
  let borderClass = " border border-top-0"
  if (idx % 3 == 0) borderClass += " border-left-md-0"
  if (idx % 3 == 2) borderClass += " border-right-md-0"
  if (idx % 4 == 0) borderClass += " border-left-lg-0"
  if (idx % 4 == 3) borderClass += " border-right-lg-0"

  return (
    <article
      className={"catalog-item py-4 text-center" + borderClass}
      style={{ cursor: "pointer" }}
    >
      <img src={image} alt={title} width="120" height="120" />
      <h5 className="mt-2">{title}</h5>
      <span className="text-muted">R$ {price.toFixed(2)}</span>
    </article>
  )
}

export default CatalogItem
