import { SegmentedControl } from "@mantine/core";

interface InputModeControlProps {
  value: string | undefined;
  onChange: ((value: string) => void) | undefined;
  disabled: boolean | undefined;
}

const InputModeControl: React.FC<InputModeControlProps> = ({
  value,
  onChange,
  disabled,
}) => {
  return (
    <SegmentedControl
      size="sm"
      value={value}
      onChange={onChange}
      disabled={disabled}
      data={["Linear Orders", "Poset"]}
      data-testid="input-mode-control"
    />
  );
};

export default InputModeControl;
