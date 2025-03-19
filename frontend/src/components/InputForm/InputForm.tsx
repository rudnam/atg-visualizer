import {
  Button,
  InputLabel,
  InputWrapper,
  SegmentedControl,
  Slider,
  Textarea,
} from "@mantine/core";
import { useState } from "react";
import { Relation } from "../../types";

interface InputFormProps {
  fetchGraphData: (size: number, upsilon: string[]) => Promise<void>;
  fetchGraphDataFromCoverRelation: (
    size: number,
    coverRelation: Relation[],
  ) => Promise<void>;
  fetchPosetCoverResults: (
    size: number,
    k: number,
    upsilon: string[],
  ) => Promise<void>;
  loading: boolean;
}

const InputForm: React.FC<InputFormProps> = ({
  fetchPosetCoverResults,
  fetchGraphData,
  fetchGraphDataFromCoverRelation,
  loading,
}) => {
  const [size, setSize] = useState<number>(4);
  const [textareaValue, setTextareaValue] = useState<string>("");
  const [mode, setMode] = useState("Upsilon");

  const textareaOnBlur = () => {
    if (mode !== "Upsilon") return;

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
      <SegmentedControl
        size="sm"
        value={mode}
        onChange={setMode}
        data={["Upsilon", "Poset"]}
        data-testid="input-mode-control"
      />
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
          data-testid="permutation-length-slider"
        />
      </InputWrapper>
      {mode === "Upsilon" ? (
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
          maxRows={8}
          data-testid="input-y"
        />
      ) : (
        <Textarea
          className="w-36 mx-auto"
          label="Cover relations"
          description="Input cover relations"
          placeholder={`1,2\n3,2\n1,4`}
          resize="vertical"
          onChange={(event) => setTextareaValue(event.currentTarget.value)}
          onBlur={textareaOnBlur}
          disabled={loading}
          autosize
          minRows={4}
          maxRows={8}
          data-testid="input-cover-relation"
        />
      )}

      <Button
        className="mx-auto"
        variant="gradient"
        gradient={{ from: "purple", to: "maroon", deg: 90 }}
        disabled={loading}
        onClick={() => {
          if (mode === "Upsilon") {
            fetchGraphData(
              size,
              textareaValue
                .split("\n")
                .map((line) => line.trim())
                .filter((line) => line !== ""),
            );
          } else {
            fetchGraphDataFromCoverRelation(
              size,
              textareaValue
                .split("\n")
                .map((line) => line.trim())
                .filter((line) => line !== "")
                .map((line) => {
                  const [x, y] = line.split(",").map(Number);
                  return [x, y] as Relation;
                }),
            );
          }
        }}
        data-testid="draw-button"
      >
        Draw
      </Button>

      {mode === "Upsilon" ? (
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
                .filter((line) => line !== ""),
            )
          }
          data-testid="solve-button"
        >
          Solve
        </Button>
      ) : (
        <></>
      )}
    </div>
  );
};

export default InputForm;
