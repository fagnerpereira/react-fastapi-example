import { useState, useEffect } from 'react'


function FruitItem({ fruit, onDeleteFruit }) {
  const [isEditing, setIsEditing] = useState(false);
  const [fruitName, setFruitName] = useState(fruit.name)
  const [fruits, setFruits] = useState([])

  const updateFruit = async () => {
    try {
      const response = await fetch(`http://localhost:8000/fruits/${fruit.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          // 'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          name: fruitName
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update todo');
      }

      const updated = await response.json();
      console.log('updated', updated)
    } catch (err) {
      // setError(err.message);
    } finally {
      // setLoading(false);
    }
  };



  const handleUpdate = () => {
    if (isEditing) {
      updateFruit(fruit.id);
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
        <button onClick={handleUpdate}>{isEditing ? 'Save' : 'Edit'}</button>
        <button onClick={() => onDeleteFruit(fruit.id)}>Remove</button>
      </td>
    </tr>
  );
}

function App() {
  const [fruitName, setFruitName] = useState('')
  const [fruits, setFruits] = useState([])
  const [isEditing, setIsEditing] = useState(false)

  useEffect(() => {
    const fetchFruits = async () => {
      const r = await fetch('http://localhost:8000/fruits')
      const data = await r.json()
      setFruits(data)
    }
    fetchFruits()
  }, [])

  const addFruit = async (e) => {
    e.preventDefault()

    try {
      const r = await fetch('http://localhost:8000/fruits', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer token'
        },
        body: JSON.stringify({
          name: fruitName
        })
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

  const deleteFruit = async (id) => {
    // setLoading(true);
    try {
      console.log(id)
      // const response = await fetch(`http://localhost:8000/fruits/${id}`, {
      //   method: 'DELETE',
      // });

      // setFruits(fruits.filter(fruit => fruit.id !== id));
    } catch (err) {
      // setError(err.message);
    } finally {
      // setLoading(false);
    }
  };
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

      <h2>My basket</h2>

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
              onDeleteFruit={deleteFruit}
            />
          ))}
        </tbody>
      </table>
    </>
  )
}

export default App
