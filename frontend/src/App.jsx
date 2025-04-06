import { useState, useEffect } from 'react'


function FruitItem({ fruit, onUpdateFruit, onDeleteFruit }) {
  const [isEditing, setIsEditing] = useState(false);
  const [fruitName, setFruitName] = useState(fruit.name)

  const handleUpdate = () => {
    if (isEditing) {
      onUpdateFruit(fruit.id, { name: fruitName });
    }
    setIsEditing(!isEditing);
  };

  return (
    <tr key={fruit.id}>
      <td>{fruit.id}</td>
      <td>
        {isEditing ? (
          <input
            type="text"
            value={fruitName}
            onChange={(e) => setFruitName(e.target.value)}
          />
        ) : (
          fruitName
        )}
      </td>
      <td>
        <button onClick={handleUpdate}>
          {isEditing ? 'Save' : 'Edit'}
        </button>
        <button onClick={() => onDeleteFruit(fruit.id)}>
          Remove
        </button>
      </td>
    </tr>
  );
}

function App() {
  const [fruitName, setFruitName] = useState('')
  const [fruits, setFruits] = useState([])
  const [loading, setLoading] = useState(false)

  const API_URL = 'http://localhost:8000'
  const token = 'token'

  useEffect(() => {
    readFruits()
  }, [])

  const readFruits = async () => {
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/fruits`)
      const data = await response.json()

      setFruits(data)
    } catch (error) {
      console.log(error)
    } finally {
      setLoading(false)
    }
  }

  const createFruit = async (e) => {
    e.preventDefault()

    const newFruit = {
      name: fruitName
    }

    setLoading(true)
    setFruitName('')

    try {
      const response = await fetch(`${API_URL}/fruits`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer token'
        },
        body: JSON.stringify({
          name: fruitName
        })
      })

      const newFruit = await response.json()
      setFruits([...fruits, newFruit])
    } catch (error) {
      console.log(error)
    } finally {
      setLoading(false)
    }
  }

  const updateFruit = async (id, updatedData) => {
    try {
      const response = await fetch(`${API_URL}/fruits/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updatedData)
      });

      const updated = await response.json();
      console.log('updated', updated)
    } catch (error) {
      console.log(error);
    }
  };

  const deleteFruit = async (id) => {
    try {
      await fetch(`${API_URL}/fruits/${id}`, {
        method: 'DELETE',
      });

      setFruits(fruits.filter(fruit => fruit.id !== id));
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <>
      <h2>Fruits</h2>
      <form onSubmit={createFruit}>
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

      <h2>My basket</h2>

      {
        loading ? (
          <p>Loading...</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {fruits.map((fruit) => (
                <FruitItem
                  key={fruit.id}
                  fruit={fruit}
                  onUpdateFruit={updateFruit}
                  onDeleteFruit={deleteFruit}
                />
              ))}
            </tbody>
          </table>
        )
      }
    </>
  )
}

export default App
