import React, { useState, useEffect } from 'react';
import './App.css';

const BACKEND_URL = "http://localhost:8000";

export function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${BACKEND_URL}/todos?page=1&limit=20`);
      const result = await response.json();
      if (result.success && Array.isArray(result.data)) {
        setTodos(result.data);
      } else {
        setTodos([]);
        setError("Unexpected response format from backend.");
      }
    } catch (err) {
      console.error("Error fetching TODOs:", err);
      setTodos([]);
      setError("Failed to fetch TODOs from backend.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    try {
      const response = await fetch(`${BACKEND_URL}/todos/create/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTodo }),
      });

      if (response.ok) {
        const result = await response.json();
        setTodos((prev) => [
          { ...result, _id: result._id || Date.now(), completed: false, title: newTodo, created_at: new Date().toISOString() },
          ...prev,
        ]);
        setNewTodo('');
      } else {
        setError("Failed to create TODO.");
      }
    } catch (err) {
      console.error('Error creating TODO:', err);
      setError("Error creating TODO.");
    }
  };

  return (
    <div className="App" style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>

      <div style={{ marginBottom: '30px' }}>
        <h1>Create a ToDo</h1>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <input
              type="text"
              id="todo"
              value={newTodo}
              placeholder="Enter new todo"
              onChange={(e) => setNewTodo(e.target.value)}
              style={{ flex: 1, padding: '8px', borderRadius: '5px', border: '1px solid #ccc' }}
            />
            <button
              type="submit"
              style={{
                padding: '8px 15px',
                borderRadius: '5px',
                backgroundColor: '#007bff',
                color: '#fff',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Add
            </button>
          </div>
        </form>
      </div>

      <div>
        <h1>List of TODOs</h1>
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p style={{ color: 'red' }}>{error}</p>
        ) : todos.length === 0 ? (
          <p>No TODOs found.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {todos.map((todo) => (
              <div
                key={todo._id}
                className="todo-card"
                style={{
                  border: `2px solid ${todo.completed ? 'green' : 'red'}`,
                  borderRadius: '8px',
                  padding: '15px',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                  backgroundColor: '#fff',
                  opacity: 0,
                  transform: 'translateY(-10px)',
                  animation: 'fadeInSlide 0.3s forwards',
                }}
              >
                <h3 style={{ margin: '0 0 5px 0' }}>{todo.title}</h3>
                <p style={{ margin: 0, fontSize: '0.9em', color: '#555' }}>
                  Created at: {new Date(todo.created_at).toLocaleString()}
                </p>
                <p
                  style={{
                    margin: '5px 0 0 0',
                    fontWeight: 'bold',
                    color: todo.completed ? 'green' : 'red',
                  }}
                >
                  {todo.completed ? 'Completed' : 'Pending'}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      <style>{`
        @keyframes fadeInSlide {
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}

export default App;
