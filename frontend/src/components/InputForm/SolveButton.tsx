import { Button } from "@mantine/core";

interface SolveButtonProps {
  onClick: React.MouseEventHandler<HTMLButtonElement> | undefined;
  disabled: boolean | undefined;
}

const SolveButton: React.FC<SolveButtonProps> = ({ onClick, disabled }) => {
  return (
    <Button
      className="mx-auto"
      variant="gradient"
      gradient={{ from: "purple", to: "maroon", deg: 90 }}
      onClick={onClick}
      disabled={disabled}
      data-testid="solve-button"
    >
      Solve
    </Button>
  );
};

export default SolveButton;
