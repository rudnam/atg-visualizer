import {
  Button,
  InputLabel,
  InputWrapper,
  ScrollArea,
  Slider,
  Textarea,
} from "@mantine/core";
import { useState } from "react";

interface InputFormProps {
  fetchEntireGraphData: (size: number, upsilon: string[]) => Promise<void>;
  fetchPosetCoverResults: (
    size: number,
    k: number,
    upsilon: string[]
  ) => Promise<void>;
  loading: boolean;
}

const InputForm: React.FC<InputFormProps> = ({
  fetchPosetCoverResults,
  fetchEntireGraphData,
  loading,
}) => {
  const [size, setSize] = useState<number>(4);
  const [textareaValue, setTextareaValue] = useState<string>("");

  const textareaOnBlur = () => {
    const upsilon = textareaValue
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line !== "");
    if (upsilon.length > 0) {
      setSize(upsilon[0].length);
    }
  };

  return (
    <div className="w-72 h-full max-h-[36rem] flex flex-col mx-auto md:mx-0 gap-4 bg-[#fefefe] p-8 rounded-xl shadow-lg">
      <div className="text-xl font-bold">INPUT</div>
      <InputWrapper>
        <InputLabel>Permutation Length</InputLabel>
        <Slider
          defaultValue={4}
          min={2}
          max={6}
          onChange={setSize}
          value={size}
          marks={[
            { value: 2, label: 2 },
            { value: 3 },
            { value: 4 },
            { value: 5 },
            { value: 6, label: 6 },
          ]}
        />
      </InputWrapper>
      <ScrollArea.Autosize mah={"60%"}>
        <Textarea
          className="w-36 mx-auto"
          label="Input Y"
          description="Input permutations"
          placeholder={`1234\n4321\n3214`}
          resize="vertical"
          onChange={(event) => setTextareaValue(event.currentTarget.value)}
          onBlur={textareaOnBlur}
          disabled={loading}
          autosize
          minRows={4}
        />
      </ScrollArea.Autosize>

      <Button
        className="mx-auto"
        variant="gradient"
        gradient={{ from: "purple", to: "maroon", deg: 90 }}
        disabled={loading}
        onClick={() =>
          fetchEntireGraphData(
            size,
            textareaValue
              .split("\n")
              .map((line) => line.trim())
              .filter((line) => line !== "")
          )
        }
      >
        Draw
      </Button>
      <Button
        className="mx-auto"
        variant="gradient"
        gradient={{ from: "purple", to: "maroon", deg: 90 }}
        disabled={loading}
        onClick={() =>
          fetchPosetCoverResults(
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
