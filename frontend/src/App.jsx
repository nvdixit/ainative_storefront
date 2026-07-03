import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Products from './views/Products/Products.jsx';
import Orders from './views/Orders/Orders.jsx';

function App() {
  return (
    <Router>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-brand">
            TestAgent Store
          </Link>
          <ul className="navbar-menu">
            <li>
              <Link to="/products" className="navbar-link">Products</Link>
            </li>
            <li>
              <Link to="/orders" className="navbar-link">My Orders</Link>
            </li>
          </ul>
        </div>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/products" element={<Products />} />
          <Route path="/orders" element={<Orders />} />
          <Route path="/" element={<Products />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
