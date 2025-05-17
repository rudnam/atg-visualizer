import { Textarea } from "@mantine/core";

interface InputCoverRelationsProps {
  onChange: React.ChangeEventHandler<HTMLTextAreaElement> | undefined;
  onBlur: React.FocusEventHandler<HTMLTextAreaElement> | undefined;
  disabled: boolean | undefined;
  error: React.ReactNode;
}

const InputCoverRelations: React.FC<InputCoverRelationsProps> = ({
  onChange,
  onBlur,
  disabled,
  error,
}) => {
  return (
    <Textarea
      className="w-36 mx-auto"
      label="Cover relations"
      description="Input cover relations"
      placeholder={`1,2\n3,2\n1,4`}
      onChange={onChange}
      onBlur={onBlur}
      disabled={disabled}
      autosize
      minRows={4}
      maxRows={7}
      error={error}
      data-testid="input-cover-relation"
    />
  );
};

export default InputCoverRelations;
