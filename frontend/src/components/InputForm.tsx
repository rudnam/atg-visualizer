import { Textarea } from "@mantine/core";

const InputForm: React.FC = () => {
  return (
    <div className="w-72 flex flex-col mt-4 mx-auto md:mx-0 gap-4">
      <div className="text-2xl font-bold">INPUT</div>

      <Textarea
        className="w-full"
        label="Input Y"
        description="E.g. 1234"
        placeholder="Input placeholder"
        resize="vertical"
      />
    </div>
  );
};

export default InputForm;
