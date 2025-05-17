import { Button } from "@mantine/core";

interface DrawButtonProps {
  onClick: React.MouseEventHandler<HTMLButtonElement> | undefined;
  disabled: boolean | undefined;
}

const DrawButton: React.FC<DrawButtonProps> = ({ onClick, disabled }) => {
  return (
    <Button
      className="mx-auto"
      variant="gradient"
      gradient={{ from: "purple", to: "maroon", deg: 90 }}
      disabled={disabled}
      onClick={onClick}
      data-testid="draw-button"
    >
      Draw
    </Button>
  );
};

export default DrawButton;
