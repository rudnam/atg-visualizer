import { Textarea } from "@mantine/core";

interface InputTextareaProps {
  label: React.ReactNode;
  description: React.ReactNode;
  placeholder: string | undefined;
  onChange: React.ChangeEventHandler<HTMLTextAreaElement> | undefined;
  onBlur: React.FocusEventHandler<HTMLTextAreaElement> | undefined;
  disabled: boolean | undefined;
  error: React.ReactNode;
}

const InputTextarea: React.FC<InputTextareaProps> = ({
  label,
  description,
  placeholder,
  onChange,
  onBlur,
  disabled,
  error,
}) => {
  return (
    <Textarea
      className="w-36 mx-auto"
      label={label}
      description={description}
      placeholder={placeholder}
      onChange={onChange}
      onBlur={onBlur}
      disabled={disabled}
      autosize
      minRows={4}
      maxRows={5}
      error={error}
      data-testid="input-textarea"
    />
  );
};

export default InputTextarea;
