import { useEffect, useState } from 'react';
import Product from '../../components/Product/Product.jsx';
import ChatWidget from '../../components/ChatWidget/ChatWidget.jsx';

function Favorites() {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchFavorites() {
      try {
        const response = await fetch('http://localhost:8000/favorites');
        if (!response.ok) {
          throw new Error(`Failed to load favorites: ${response.status}`);
        }
        const data = await response.json();
        setFavorites(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchFavorites();
  }, []);

  return (
    <div className="favorites-page">
      <h1>Your Favorites</h1>
      <br />
      <br />

      {loading && <p>Loading favorites...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && favorites.length === 0 && (
        <p>You have no favorite products yet.</p>
      )}

      {!loading && !error && favorites.length > 0 && (
        <div className="products-grid">
          {favorites.map((product) => (
            <Product key={product.product_id} product={product} />
          ))}
        </div>
      )}

      <ChatWidget />
    </div>
  );
}

export default Favorites;
