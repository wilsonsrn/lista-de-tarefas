import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <h1 className="text-2xl text-white font-bold">
      Hello Vite + React + Tailwind!
    </h1>
    <div class="bg-dracula-pink">
    <p class="text-dracula-buffy">I vant to suck your blood...</p>
    <p class="text-pink-500">Tailwind is cool...</p> //still works!
</div>
    </>
  )
}

export default App
