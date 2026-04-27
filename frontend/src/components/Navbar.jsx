import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { sessionQuit } from '../api'

function Navbar({ role, setRole, onSessionData }) {
  const location = useLocation()
  const navigate = useNavigate()
  const isActive = (path) => location.pathname === path ? 'active' : ''

  const handleQuit = async () => {
    const data = await sessionQuit()
    if (onSessionData) onSessionData(data)
    setRole('none')
    navigate('/')
  }

  return (
    <div className="navbar">
      <Link to="/" className="brand">CAMPUS CAFE</Link>
      <nav>
        <Link to="/" className={isActive('/')}>Home</Link>
        {role === 'customer' && (
          <>
            <Link to="/menu" className={isActive('/menu')}>Menu</Link>
            <Link to="/cart" className={isActive('/cart')}>Cart</Link>
          </>
        )}
        <Link to={role === 'staff' ? '/staff/dashboard' : '/staff/login'} className={isActive('/staff/login') || isActive('/staff/dashboard')}>
          Staff
        </Link>
        {role === 'staff' && (
          <button className="nav-quit-btn" onClick={handleQuit}>Quit</button>
        )}
      </nav>
    </div>
  )
}

export default Navbar
