import PriceFormatted from "./PriceFormatted"

function CatalogItem({ title, price_per_day, image, idx }) {
  let borderClass = " border border-top-0"
  if (idx % 3 === 0) borderClass += " border-left-md-0"
  if (idx % 3 === 2) borderClass += " border-right-md-0"
  if (idx % 4 === 0) borderClass += " border-left-lg-0"
  if (idx % 4 === 3) borderClass += " border-right-lg-0"

  return (
    <article
      className={"catalog-item py-4 text-center" + borderClass}
      style={{ cursor: "pointer" }}
    >
      <img src={image} alt={title} width="120" height="120" />
      <h6 className="mt-2 px-2 text-wrap">{title}</h6>
      <span className="text-muted">
        <PriceFormatted value={price_per_day} />
      </span>
    </article>
  )
}

export default CatalogItem
