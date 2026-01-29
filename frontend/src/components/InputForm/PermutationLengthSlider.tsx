import { InputLabel, InputWrapper, Slider } from "@mantine/core";

interface PermutationLengthSliderProps {
  value: number | undefined;
  onChange: ((value: number) => void) | undefined;
  disabled: boolean | undefined;
}

const PermutationLengthSlider: React.FC<PermutationLengthSliderProps> = ({
  value,
  onChange,
  disabled,
}) => {
  return (
    <InputWrapper>
      <InputLabel>Linear Order Length</InputLabel>
      <Slider
        defaultValue={4}
        min={2}
        max={6}
        onChange={onChange}
        value={value}
        disabled={disabled}
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
  );
};

export default PermutationLengthSlider;
