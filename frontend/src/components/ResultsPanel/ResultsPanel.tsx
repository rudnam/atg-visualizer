import { Button, Divider, Group, ScrollArea, Textarea } from "@mantine/core";
import React from "react";
import { PosetResult } from "../../types";

interface ResultsPanelProps {
  posetResults: PosetResult[];
  highlightedPosetIndex: number;
  setHighlightedPosetIndex: React.Dispatch<React.SetStateAction<number>>;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({
  posetResults,
  highlightedPosetIndex,
  setHighlightedPosetIndex,
}) => {
  const items = posetResults.map((item, index) => {
    const withDivider = index !== posetResults.length - 1;

    const buttonOnClick = () => {
      if (index === highlightedPosetIndex) {
        setHighlightedPosetIndex(-1);
      } else {
        setHighlightedPosetIndex(index);
      }
    };

    const buttonVariant =
      index === highlightedPosetIndex ? "filled" : "outline";

    return PosetResultComponent(
      item,
      withDivider,
      buttonVariant,
      buttonOnClick
    );
  });

  return (
    <div className="h-full w-72 max-h-[36rem] mx-auto md:mx-0 gap-4 bg-[#fefefe] p-8 rounded-xl shadow-lg">
      <div className="text-xl font-bold">RESULTS</div>
      <ScrollArea scrollbarSize={4} offsetScrollbars className="h-full py-4">
        {items}
      </ScrollArea>
    </div>
  );
};

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
    <div key={`PosetResult${name}`}>
      <Group justify="space-between">
        <p>{name}</p>
        <Button
          size="compact-xs"
          radius="lg"
          onClick={() => {
            buttonOnClick();
          }}
          variant={buttonVariant}
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
      />
      {withDivider ? <Divider my="sm" size="sm" /> : <></>}
    </div>
  );
}

export default ResultsPanel;
