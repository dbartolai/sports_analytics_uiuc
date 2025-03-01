import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Header from './Header.jsx'
import Drake from './Drake.jsx'
import Cal from './Cal.jsx'
import DanielC from './DanielC.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Header />
    <Drake />
    <App />
    <Cal />
    <DanielC />
  </StrictMode>,
)
