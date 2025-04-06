import { useState } from 'react'

function App() {
  const [fruitName, setFruitName] = useState('')
  const [fruits, setFruits] = useState([])

  const addFruit = async (e) => {
    e.preventDefault()
    console.log(fruitName)
    try {
      const r = await fetch('http://localhost:8000/api/fruits', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer token'
        },
        body: JSON.stringify(fruitName)
      })

      if (!r.ok) {
        throw new Error("Failed to add fruit");
      }

      const newFruit = await r.json()
      setFruits([...fruits, newFruit])
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <>
      <h2>Fruits</h2>
      <form onSubmit={addFruit}>
        <label>
          Name:
          <input
            type="text"
            value={fruitName}
            onChange={(e) => setFruitName(e.target.value)}
            required
          />
        </label>
        <button>Add fruit</button>
      </form>
    </>
  )
}

export default App
