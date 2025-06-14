import { useMemo, useState } from "react";
import { DrawingMethod, InputMode, Relation } from "../../types";
import { useDebouncedCallback } from "@mantine/hooks";
import InputModeControl from "./InputModeControl";
import PermutationLengthSlider from "./PermutationLengthSlider";
import InputSelectDrawingMethod from "./InputSelectDrawingMethod";
import DrawButton from "./DrawButton";
import SolveButton from "./SolveButton";
import InputTextarea from "./InputTextarea";

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
  const [drawingMethod, setDrawingMethod] = useState<DrawingMethod>("Default");
  const [mode, setMode] = useState<InputMode>("Linear Orders");
  const [textareaError, setTextareaError] = useState<string>("");

  const parsedLines = useMemo(
    () =>
      textareaValue
        .split("\n")
        .map((l) => l.trim())
        .filter(Boolean),
    [textareaValue],
  );

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
    if (parsedLines.length && mode === "Linear Orders") {
      const errorMessage = validateLinearOrderArray(parsedLines, size);
      if (errorMessage) {
        setTextareaError(errorMessage);
        return;
      }
    } else if (parsedLines.length && mode === "Poset") {
      const errorMessage = validateCoverRelationArray(parsedLines, size);
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
      <InputModeControl
        value={mode}
        onChange={(value: string) => {
          setMode(value as InputMode);
          validateInput();
        }}
        disabled={loading}
      />
      <PermutationLengthSlider
        value={size}
        onChange={(value: number) => {
          setSize(value);
          validateInput();
        }}
        disabled={loading}
      />
      <InputTextarea
        label={mode === "Linear Orders" ? "Linear orders" : "Cover relations"}
        description={
          mode === "Linear Orders"
            ? "Input linear orders"
            : "Input cover relations"
        }
        placeholder={
          mode === "Linear Orders" ? "1234\n4321\n3214" : "1,2\n3,2\n1,4"
        }
        onChange={(event) => {
          setTextareaValue(event.currentTarget.value);
          validateInput();
        }}
        onBlur={() => {
          updateSize();
        }}
        disabled={loading}
        error={textareaError}
      />

      <InputSelectDrawingMethod
        value={drawingMethod}
        onChange={(value) => {
          setDrawingMethod(value as DrawingMethod);
        }}
        disabled={loading}
      />
      <DrawButton
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
        disabled={loading || textareaError !== ""}
      />

      {mode === "Linear Orders" && (
        <SolveButton
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
          disabled={loading || textareaError !== ""}
        />
      )}
    </div>
  );
};

export default InputForm;
