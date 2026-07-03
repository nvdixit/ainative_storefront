import './Order.css';

function Order({ order, isExpanded, onToggleExpand }) {
  return (
    <>
      <tr className="order-row">
        <td className="order-expand-cell">
          <button 
            className="expand-button" 
            onClick={onToggleExpand}
            aria-expanded={isExpanded}
          >
            {isExpanded ? '▼' : '▶'}
          </button>
        </td>
        <td>{order.order_id}</td>
        <td>{order.order_date}</td>
        <td>{order.status}</td>
        <td>${order.subtotal_usd.toFixed(2)}</td>
        <td>${order.shipping_usd.toFixed(2)}</td>
        <td>${order.total_usd.toFixed(2)}</td>
      </tr>
      {isExpanded && order.products && order.products.length > 0 && (
        <tr className="order-items-row">
          <td colSpan="7">
            <div className="order-items-container">
              <h3>Items in this order</h3>
              <table className="items-table">
                <thead>
                  <tr>
                    <th>Product ID</th>
                    <th>Product Name</th>
                    <th>Category</th>
                    <th>Brand</th>
                    <th>Unit Price</th>
                    <th>Quantity</th>
                    <th>Line Total</th>
                  </tr>
                </thead>
                <tbody>
                  {order.products.map((product) => (
                    <tr key={product.product_id}>
                      <td>{product.product_id}</td>
                      <td>{product.product_name}</td>
                      <td>{product.category}</td>
                      <td>{product.brand}</td>
                      <td>${product.unit_price_usd.toFixed(2)}</td>
                      <td>{product.quantity}</td>
                      <td>${product.line_total_usd.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </td>
        </tr>
      )}
    </>
  );
}

export default Order;
