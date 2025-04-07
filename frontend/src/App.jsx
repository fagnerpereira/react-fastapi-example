import { useState, useEffect } from 'react'

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(username, password);
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Username:
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </label>
        </div>
        <div>
          <label>
            Password:
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
        </div>
        <button type="submit">Login</button>
      </form>
      <p>Use username: alice, password: secret2</p>
    </div>
  );
}

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
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [fruitName, setFruitName] = useState('')
  const [fruits, setFruits] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const API_URL = 'http://localhost:8000'

  useEffect(() => {
    if (token) {
      readFruits()
    }
  }, [token])

  const handleLogin = async (username, password) => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/token?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      setToken(data.access_token);
      localStorage.setItem('token', data.access_token);
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    setFruits([]);
  };

  const readFruits = async () => {
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/fruits`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
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
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newFruit)
      })

      const createdFruit = await response.json()
      setFruits([...fruits, createdFruit])
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
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setFruits(fruits.filter(fruit => fruit.id !== id));
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <h1>Fruits App</h1>

      {error && <p>{error}</p>}

      {!token ? (
        <Login onLogin={handleLogin} />
      ) : (
        <div>
          <button onClick={handleLogout}>Logout</button>
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
        </div>
      )}
    </>
  )
}

export default App
