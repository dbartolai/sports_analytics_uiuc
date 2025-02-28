import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Header from './Header.jsx'
import DanielC from './DanielC'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Header />
    <App />
    <DanielC />
  </StrictMode>,
)
