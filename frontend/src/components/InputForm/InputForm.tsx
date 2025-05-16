import {
  Button,
  InputLabel,
  InputWrapper,
  SegmentedControl,
  Select,
  Slider,
  Textarea,
} from "@mantine/core";
import { useState } from "react";
import { DrawingMethod, Relation } from "../../types";
import { useDebouncedCallback } from "@mantine/hooks";

interface InputFormProps {
  fetchGraphData: (
    size: number,
    drawingMethod: DrawingMethod,
    upsilon: string[],
  ) => Promise<void>;
  fetchGraphDataFromCoverRelation: (
    size: number,
    drawingMethod: DrawingMethod,
    coverRelation: Relation[],
  ) => Promise<void>;
  fetchPosetCoverResults: (
    size: number,
    drawingMethod: DrawingMethod,
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
  const [drawingMethod, setDrawingMethod] = useState<string | null>("Default");
  const [mode, setMode] = useState("Linear Orders");
  const [textareaError, setTextareaError] = useState<string>("");

  const updateSize = () => {
    if (mode == "Linear Orders") {
      const upsilon = textareaValue
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line !== "");

      if (upsilon.length > 0) {
        setSize(upsilon[0].length);
      }
    } else if (mode == "Poset") {
      const numbers = textareaValue
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line !== "")
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        .map(([num1, _, num2]) => [parseInt(num1), parseInt(num2)])
        .flat();

      if (numbers.length > 0 && size < Math.max(...numbers)) {
        setSize(Math.max(...numbers));
      }
    }
    validateInput();
  };

  const validateLinearOrderArray = (arr: string[], size: number) => {
    const expected = new Set();
    for (let i = 1; i <= size; i++) {
      expected.add(i.toString());
    }

    for (let i = 0; i < arr.length; i++) {
      const str = arr[i];
      if (str.length !== size)
        return `'${str}' does not match specified length`;

      const chars = str.split("");
      const unique = new Set(chars);
      const all_unique =
        unique.size === size && chars.every((c) => expected.has(c));
      if (!all_unique)
        return `Invalid linear order '${str}'. Linear orders must contain digits 1-${size}.`;
    }
    return null;
  };

  const validateCoverRelationArray = (arr: string[], size: number) => {
    for (let i = 0; i < arr.length; i++) {
      const str = arr[i];
      const parts = str.split(",");
      if (parts.length !== 2) return `Invalid relation '${str}'`;

      const [a, b] = parts.map(Number);
      const isNumbers =
        Number.isInteger(a) && Number.isInteger(b) && a >= 1 && b >= 1;
      if (!isNumbers) return `Invalid relation '${str}'`;

      const isCorrectSize = a <= size && b <= size;
      if (!isCorrectSize)
        return `'${str}' implies that the linear order length is ${a > b ? a : b}`;
    }
    return null;
  };

  const validateInput = useDebouncedCallback(() => {
    const lines = textareaValue
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);

    if (lines.length && mode === "Linear Orders") {
      const errorMessage = validateLinearOrderArray(lines, size);
      if (errorMessage) {
        setTextareaError(errorMessage);
        return;
      }
    } else if (lines.length && mode === "Poset") {
      const errorMessage = validateCoverRelationArray(lines, size);
      if (errorMessage) {
        setTextareaError(errorMessage);
        return;
      }
    }

    setTextareaError("");
  }, 500);

  return (
    <div className="w-72 h-full max-h-[36rem] flex flex-col mx-auto md:mx-0 gap-4 bg-[#fefefe] p-8 rounded-xl shadow-lg">
      <div className="text-xl font-bold">INPUT</div>
      <SegmentedControl
        size="sm"
        value={mode}
        onChange={setMode}
        disabled={loading}
        data={["Linear Orders", "Poset"]}
        data-testid="input-mode-control"
      />
      <InputWrapper>
        <InputLabel>Linear Order Length</InputLabel>
        <Slider
          defaultValue={4}
          min={2}
          max={6}
          onChange={(value: number) => {
            setSize(value);
            validateInput();
          }}
          value={size}
          disabled={loading}
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
      {mode === "Linear Orders" ? (
        <Textarea
          className="w-36 mx-auto"
          label="Linear orders"
          description="Input linear orders"
          placeholder={`1234\n4321\n3214`}
          onChange={(event) => {
            setTextareaValue(event.currentTarget.value);
            validateInput();
          }}
          onBlur={() => {
            updateSize();
          }}
          disabled={loading}
          autosize
          minRows={4}
          maxRows={5}
          error={textareaError}
          data-testid="input-linear-orders"
        />
      ) : (
        <Textarea
          className="w-36 mx-auto"
          label="Cover relations"
          description="Input cover relations"
          placeholder={`1,2\n3,2\n1,4`}
          onChange={(event) => {
            setTextareaValue(event.currentTarget.value);
            validateInput();
          }}
          onBlur={() => {
            updateSize();
          }}
          disabled={loading}
          autosize
          minRows={4}
          maxRows={7}
          error={textareaError}
          data-testid="input-cover-relation"
        />
      )}
      <Select
        className="w-40 mx-auto"
        label="Drawing method"
        value={drawingMethod}
        onChange={setDrawingMethod}
        disabled={loading}
        data={["Default", "Supercover", "SuperHex", "Permutahedron"]}
        data-testid="input-select-drawing-method"
        comboboxProps={{
          shadow: "md",
          transitionProps: { transition: "pop", duration: 200 },
        }}
      />

      <Button
        className="mx-auto"
        variant="gradient"
        gradient={{ from: "purple", to: "maroon", deg: 90 }}
        disabled={loading || textareaError !== ""}
        onClick={() => {
          if (mode === "Linear Orders") {
            fetchGraphData(
              size,
              drawingMethod as DrawingMethod,
              textareaValue
                .split("\n")
                .map((line) => line.trim())
                .filter((line) => line !== ""),
            );
          } else {
            fetchGraphDataFromCoverRelation(
              size,
              drawingMethod as DrawingMethod,
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

      {mode === "Linear Orders" ? (
        <Button
          className="mx-auto"
          variant="gradient"
          gradient={{ from: "purple", to: "maroon", deg: 90 }}
          disabled={loading || textareaError !== ""}
          onClick={() =>
            fetchPosetCoverResults(
              size,
              drawingMethod as DrawingMethod,
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
