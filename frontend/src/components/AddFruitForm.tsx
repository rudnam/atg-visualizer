import React, { useState } from "react";

interface AddFruitFormProps {
  addFruit: (fruit: string) => void;
}

const AddFruitForm: React.FC<AddFruitFormProps> = ({ addFruit }) => {
  const [fruitName, setFruitName] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (fruitName) {
      addFruit(fruitName);
      setFruitName("");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={fruitName}
        onChange={(e) => setFruitName(e.target.value)}
        placeholder="Enter fruit name"
      />
      <button type="submit">Add Fruit</button>
    </form>
  );
};

export default AddFruitForm;
