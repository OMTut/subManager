import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/layout1.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
