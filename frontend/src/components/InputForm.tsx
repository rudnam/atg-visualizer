import {
  Button,
  InputLabel,
  InputWrapper,
  Slider,
  Textarea,
} from "@mantine/core";
import { useState } from "react";

interface InputFormProps {
  fetchEntireGraphData: (size: number) => Promise<void>;
  fetchPosetResults: (
    size: number,
    k: number,
    upsilon: string[]
  ) => Promise<void>;
}

const InputForm: React.FC<InputFormProps> = ({
  fetchPosetResults,
  fetchEntireGraphData,
}) => {
  const [size, setSize] = useState<number>(4);
  const [textareaValue, setTextareaValue] = useState<string>("");

  return (
    <div className="w-72 h-full max-h-[36rem] flex flex-col mx-auto md:mx-0 gap-4 bg-[#fefefe] p-8 rounded-xl shadow-lg">
      <div className="text-xl font-bold">INPUT</div>
      <InputWrapper>
        <InputLabel>Size</InputLabel>
        <Slider
          defaultValue={4}
          min={2}
          max={6}
          onChange={setSize}
          marks={[
            { value: 2, label: 2 },
            { value: 3 },
            { value: 4 },
            { value: 5 },
            { value: 6, label: 6 },
          ]}
        />
      </InputWrapper>

      <Textarea
        className="w-36 mx-auto"
        label="Input Y"
        description="Input permutations"
        placeholder={`1234\n4321\n3214`}
        resize="vertical"
        onChange={(event) => setTextareaValue(event.currentTarget.value)}
        autosize
        minRows={4}
      />
      <Button
        className="mx-auto"
        variant="gradient"
        gradient={{ from: "purple", to: "maroon", deg: 90 }}
        onClick={() => fetchEntireGraphData(size)}
      >
        Draw
      </Button>
      <Button
        className="mx-auto"
        variant="gradient"
        gradient={{ from: "purple", to: "maroon", deg: 90 }}
        onClick={() =>
          fetchPosetResults(
            size,
            2,
            textareaValue
              .split("\n")
              .map((line) => line.trim())
              .filter((line) => line !== "")
          )
        }
      >
        Solve
      </Button>
    </div>
  );
};

export default InputForm;
