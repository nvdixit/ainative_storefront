import './Product.css';

function Product({ product }) {
  return (
    <article className="product-card">
      <div className="product-card__header">
        <span className="product-card__id">{product.product_id}</span>
        <span className="product-card__rating">⭐ {product.rating.toFixed(1)}</span>
      </div>
      <h2 className="product-card__name">{product.product_name}</h2>
      <p className="product-card__meta">{product.brand} · {product.category}</p>
      <div className="product-card__details">
        <span className="product-card__price">${product.price_usd.toFixed(2)}</span>
        <span className="product-card__inventory">{product.inventory} in stock</span>
      </div>
    </article>
  );
}

export default Product;