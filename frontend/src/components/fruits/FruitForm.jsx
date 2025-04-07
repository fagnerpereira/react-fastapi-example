import { useState } from "react";

function FruitForm({ onCreateFruit }) {
  const [fruitName, setFruitName] = useState('');

  const handleSubmit = (e) => {
    // console.log(e)
    e.preventDefault();
    onCreateFruit({ name: fruitName });
    setFruitName('');
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
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

export default FruitForm
