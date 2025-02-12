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
  onClickDrawButton: (size: number, upsilon: string[]) => Promise<void>;
  onClickSolveButton: (
    size: number,
    k: number,
    upsilon: string[]
  ) => Promise<void>;
}

const InputForm: React.FC<InputFormProps> = ({
  onClickSolveButton,
  onClickDrawButton,
}) => {
  const [size, setSize] = useState<number>(4);
  const [textareaValue, setTextareaValue] = useState<string>("");
  const [isBusyDrawingOrSolving, setIsBusyDrawingOrSolving] = useState(false);

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
          autosize
          minRows={4}
        />
      </ScrollArea.Autosize>

      <Button
        className="mx-auto"
        variant="gradient"
        gradient={{ from: "purple", to: "maroon", deg: 90 }}
        disabled={isBusyDrawingOrSolving}
        onClick={async () => {
          setIsBusyDrawingOrSolving(true);
          await onClickDrawButton(
            size,
            textareaValue
              .split("\n")
              .map((line) => line.trim())
              .filter((line) => line !== "")
          );
          setIsBusyDrawingOrSolving(false);
        }}
      >
        Draw
      </Button>
      <Button
        className="mx-auto"
        variant="gradient"
        gradient={{ from: "purple", to: "maroon", deg: 90 }}
        disabled={isBusyDrawingOrSolving}
        onClick={async () => {
          setIsBusyDrawingOrSolving(true);
          await onClickSolveButton(
            size,
            2,
            textareaValue
              .split("\n")
              .map((line) => line.trim())
              .filter((line) => line !== "")
          );
          setIsBusyDrawingOrSolving(false);
        }}
      >
        Solve
      </Button>
    </div>
  );
};

export default InputForm;
