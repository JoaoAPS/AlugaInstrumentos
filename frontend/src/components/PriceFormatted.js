function PriceFormatted({ value }) {
  return <span>R$ {parseFloat(value).toFixed(2).replace(".", ",")}</span>
}

export default PriceFormatted
