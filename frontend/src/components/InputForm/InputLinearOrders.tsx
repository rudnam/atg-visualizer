import { Textarea } from "@mantine/core";

interface InputLinearOrdersProps {
  onChange: React.ChangeEventHandler<HTMLTextAreaElement> | undefined;
  onBlur: React.FocusEventHandler<HTMLTextAreaElement> | undefined;
  disabled: boolean | undefined;
  error: React.ReactNode;
}

const InputLinearOrders: React.FC<InputLinearOrdersProps> = ({
  onChange,
  onBlur,
  disabled,
  error,
}) => {
  return (
    <Textarea
      className="w-36 mx-auto"
      label="Linear orders"
      description="Input linear orders"
      placeholder={`1234\n4321\n3214`}
      onChange={onChange}
      onBlur={onBlur}
      disabled={disabled}
      autosize
      minRows={4}
      maxRows={5}
      error={error}
      data-testid="input-linear-orders"
    />
  );
};

export default InputLinearOrders;
