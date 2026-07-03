import { useEffect, useState } from 'react';
import Order from '../../components/Order/Order.jsx';
import ChatWidget from '../../components/ChatWidget/ChatWidget.jsx';
import './Orders.css';

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedOrderId, setExpandedOrderId] = useState(null);

  useEffect(() => {
    async function fetchOrders() {
      try {
        const response = await fetch('http://localhost:8000/orders');
        if (!response.ok) {
          throw new Error(`Failed to load orders: ${response.status}`);
        }
        const data = await response.json();
        setOrders(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchOrders();
  }, []);

  const toggleExpand = (orderId) => {
    setExpandedOrderId(expandedOrderId === orderId ? null : orderId);
  };

  return (
    <div className="orders-page">
      <h1>My Orders</h1>

      {loading && <p>Loading orders...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <div className="orders-table-wrapper">
          <table className="orders-table">
            <thead>
              <tr>
                <th></th>
                <th>Order ID</th>
                <th>Date</th>
                <th>Status</th>
                <th>Subtotal</th>
                <th>Shipping</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <Order 
                  key={order.order_id} 
                  order={order}
                  isExpanded={expandedOrderId === order.order_id}
                  onToggleExpand={() => toggleExpand(order.order_id)}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
      <ChatWidget />
    </div>
  );
}

export default Orders;
