import FruitItem from "./FruitItem"

function FruitList({ currentUser, fruits, onUpdateFruit, onDeleteFruit, loading }) {
  if (loading) {
    return <p>Loading...</p>
  }

  return (
    <>
      <h2>{currentUser.full_name}'s fruit basket</h2>

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
              onUpdateFruit={onUpdateFruit}
              onDeleteFruit={onDeleteFruit}
            />
          ))}
        </tbody>
      </table>
    </>
  )
}

export default FruitList
