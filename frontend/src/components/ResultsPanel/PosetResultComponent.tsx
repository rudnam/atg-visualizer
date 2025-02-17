import { Button, Divider, Group, Textarea } from "@mantine/core";

interface PosetResultComponentProps {
  name: string;
  linearExtensions: string[];
}

function PosetResultComponent(
  { name, linearExtensions }: PosetResultComponentProps,
  withDivider: boolean,
  buttonVariant: string,
  buttonOnClick: () => void
) {
  return (
    <div key={`PosetResult${name}`} data-testid="poset-result-component">
      <Group justify="space-between">
        <p>{name}</p>
        <Button
          size="compact-xs"
          radius="lg"
          onClick={() => {
            buttonOnClick();
          }}
          variant={buttonVariant}
          data-testid="poset-result-component-button"
        >
          Show {name}
        </Button>
      </Group>
      <Textarea
        className="w-36"
        description="Linear Extensions"
        value={linearExtensions.join("\n")}
        autosize
        minRows={3}
        readOnly
        data-testid="poset-result-component-linear-extensions"
      />
      {withDivider ? <Divider my="sm" size="sm" /> : <></>}
    </div>
  );
}

export default PosetResultComponent;
