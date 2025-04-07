import { useState } from 'react';

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

export default FruitItem
