import { useEffect, useState } from 'react';
import './Products.css';
import Product from '../../components/Product/Product.jsx';
import ChatWidget from '../../components/ChatWidget/ChatWidget.jsx';

function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchProducts() {
      try {
        const response = await fetch('http://localhost:8000/products');
        if (!response.ok) {
          throw new Error(`Failed to load products: ${response.status}`);
        }
        const data = await response.json();
        setProducts(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchProducts();
  }, []);

  return (
    <div className="products-page">
      <h1>Shop Products</h1>
      <br />
      <br />

      {loading && <p>Loading products...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <div className="products-grid">
          {products.map((product) => (
            <Product key={product.product_id} product={product} />
          ))}
        </div>
      )}
      <ChatWidget />
    </div>
  );
}

export default Products;
