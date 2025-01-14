import React, { useState } from "react";
import { TextInput, Button } from "@mantine/core";

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
    <form
      onSubmit={handleSubmit}
      className="max-w-md mx-auto mt-4 p-4 bg-white shadow-md rounded-lg"
    >
      <TextInput
        label="Fruit Name"
        placeholder="Enter fruit name"
        value={fruitName}
        onChange={(e) => setFruitName(e.target.value)}
        required
      />
      <Button type="submit" fullWidth className="mt-4">
        Add Fruit
      </Button>
    </form>
  );
};

export default AddFruitForm;
