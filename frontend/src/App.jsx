import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <h1 className="text-2xl text-white font-bold">
      Hello Vite + React + Tailwind!
    </h1>
    </>
  )
}

export default App