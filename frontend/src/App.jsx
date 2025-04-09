import { useState, useEffect } from 'react'
import FruitList from './components/fruits/FruitList.jsx'
import FruitForm from './components/fruits/FruitForm.jsx';
import LoginForm from './components/auth/LoginForm.jsx';
import { API_URL, getAuthHeaders } from './services/api.js';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [currentUser, setCurrentUser] = useState({})
  const [fruitName, setFruitName] = useState('')
  const [fruits, setFruits] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (token) {
      readCurrentUser()
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

  const readCurrentUser = async () => {
    try {
      const response = await fetch(`${API_URL}/users/me`, {
        headers: getAuthHeaders()
      })

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json()
      setCurrentUser(data)
    } catch (error) {
      handleLogout()
      console.log(error)
    }
  }

  const readFruits = async () => {
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/fruits`, {
        headers: getAuthHeaders()
      })
      const data = await response.json()

      setFruits(data)
    } catch (error) {
      console.log(error)
    } finally {
      setLoading(false)
    }
  }

  const createFruit = async (fruitData) => {
    setLoading(true)
    setFruitName('')

    try {
      const response = await fetch(`${API_URL}/fruits`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders()
        },
        body: JSON.stringify(fruitData)
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
          ...getAuthHeaders()
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
        headers: getAuthHeaders()
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
        <LoginForm onLogin={handleLogin} />
      ) : (
        <div>
          <button onClick={handleLogout}>Logout</button>

          <FruitForm
            onCreateFruit={createFruit}
          />

          <FruitList
            currentUser={currentUser}
            fruits={fruits}
            loading={loading}
            onUpdateFruit={updateFruit}
            onDeleteFruit={deleteFruit}
          />
        </div>
      )}
    </>
  )
}

export default App
