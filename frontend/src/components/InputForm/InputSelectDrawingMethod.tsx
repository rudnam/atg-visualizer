import { ComboboxItem, Select } from "@mantine/core";

interface InputSelectDrawingMethodProps {
  value: string | null | undefined;
  onChange: ((value: string | null, option: ComboboxItem) => void) | undefined;
  disabled: boolean | undefined;
}

const InputSelectDrawingMethod: React.FC<InputSelectDrawingMethodProps> = ({
  value,
  onChange,
  disabled,
}) => {
  return (
    <Select
      className="w-40 mx-auto"
      label="Drawing method"
      value={value}
      onChange={onChange}
      disabled={disabled}
      data={["Default", "Supercover", "SuperHex", "Permutahedron"]}
      allowDeselect={false}
      data-testid="input-select-drawing-method"
      comboboxProps={{
        shadow: "md",
        transitionProps: { transition: "pop", duration: 200 },
      }}
    />
  );
};

export default InputSelectDrawingMethod;
