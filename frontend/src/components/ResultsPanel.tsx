import { Button, Divider, Group, ScrollArea, Textarea } from "@mantine/core";
import React, { useState } from "react";
import { PosetResult } from "../types";

interface ResultsPanelProps {
  posetResults: PosetResult[];
  setGraphIndex: React.Dispatch<React.SetStateAction<number>>;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({
  posetResults,
  setGraphIndex,
}) => {
  const [activeButtonIndex, setActiveButtonIndex] = useState(0);

  const items = posetResults.map((item, index) => {
    const withDivider = index !== posetResults.length - 1;

    const buttonOnClick = () => {
      if (index !== activeButtonIndex) {
        setActiveButtonIndex(index);
        setGraphIndex(index);
      }
    };

    const buttonVariant = index === activeButtonIndex ? "filled" : "outline";

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
        minRows={4}
        readOnly
      />
      {withDivider ? <Divider my="sm" size="sm" /> : <></>}
    </div>
  );
}

export default ResultsPanel;
