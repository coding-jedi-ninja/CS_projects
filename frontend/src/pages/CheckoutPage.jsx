import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { checkout } from '../api'

function CheckoutPage() {
  const navigate = useNavigate()
  const [telephone, setTelephone] = useState('')
  const [receipt, setReceipt] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (receipt) {
      const timer = setTimeout(() => navigate('/'), 8000)
      return () => clearTimeout(timer)
    }
  }, [receipt, navigate])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    const num = parseInt(telephone)
    if (!num || num <= 0) {
      setError('Please enter a valid telephone number.')
      return
    }

    const result = await checkout(num)
    if (result.success) {
      setReceipt(result.receipt)
    } else {
      setError(result.message)
    }
  }

  if (receipt) {
    return (
      <div className="page">
        <h2>Receipt</h2>
        <div className="receipt">
          <h3>CAMPUS CAFE</h3>
          <div className="address">4 N Second Street, San Jose, CA 95113</div>
          <hr className="divider" />
          <div className="receipt-row">
            <span>Date: {receipt.date}</span>
            <span>Time: {receipt.time}</span>
          </div>
          <div className="receipt-row">
            <span>Customer ID: {receipt.customer_id}</span>
            <span>Points: {receipt.points}</span>
          </div>
          <hr className="divider" />
          {receipt.items.map(item => (
            <div className="receipt-row" key={item.name}>
              <span>{item.name} x{item.quantity}</span>
              <span>${item.price.toFixed(2)}</span>
            </div>
          ))}
          <hr className="divider" />
          <div className="receipt-row">
            <span>Subtotal</span>
            <span>${receipt.subtotal.toFixed(2)}</span>
          </div>
          {receipt.discount > 0 && (
            <div className="receipt-row">
              <span>Daily Special Discount</span>
              <span>-${receipt.discount.toFixed(2)}</span>
            </div>
          )}
          <div className="receipt-row">
            <span>Tax</span>
            <span>${receipt.tax.toFixed(2)}</span>
          </div>
          <hr className="divider" />
          <div className="receipt-row bold">
            <span>Total</span>
            <span>${receipt.total.toFixed(2)}</span>
          </div>
          <div className="thank-you">Thank you for dining with us!</div>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <h2>Checkout</h2>
      <div className="checkout-form">
        <form onSubmit={handleSubmit}>
          <h3 style={{ textAlign: 'center', color: 'var(--brown-dark)', marginBottom: 50 }}>Earn Loyalty Points</h3>
          <input
            type="text"
            value={telephone}
            onChange={(e) => setTelephone(e.target.value)}
            placeholder="Enter your phone number"
          />
          {error && <div className="message error">{error}</div>}
          <div style={{ display: 'flex', gap: 10 }}>
            <button type="submit" className="btn-success">
              Pay Now
            </button>
            <button type="button" className="btn-secondary" onClick={() => navigate('/cart')}>
              Back to Cart
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CheckoutPage
