import { Button, Divider, Group, ScrollArea, Textarea } from "@mantine/core";
import React, { useState } from "react";
import { PosetResult } from "../types";

// const posetResults = [
//   {
//     name: "P1",
//     baseSet: [1, 2, 3, 4],
//     linearExtensions: ["1234", "1243", "1423", "4123"],
//     relations: [
//       [1, 2],
//       [1, 3],
//       [2, 3],
//     ],
//     coverRelations: [],
//     highlightLEG: () => {},
//   },
//   {
//     name: "P2",
//     baseSet: [1, 2, 3, 4],
//     linearExtensions: ["1234"],
//     relations: [
//       [1, 2],
//       [1, 3],
//       [1, 4],
//       [2, 3],
//       [2, 4],
//       [3, 4],
//     ],
//     coverRelations: [],
//     highlightLEG: () => {},
//   },
//   {
//     name: "P3",
//     baseSet: [1, 2, 3, 4],
//     linearExtensions: ["1234", "1243", "1423", "1432", "1342", "1324"],
//     relations: [
//       [1, 2],
//       [1, 3],
//       [1, 4],
//     ],
//     coverRelations: [],
//     highlightLEG: () => {},
//   },
// ];

interface ResultsPanelProps {
  posetResults: PosetResult[];
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({ posetResults }) => {
  const [activeButtonIndex, setActiveButtonIndex] = useState(-1);

  const items = posetResults.map((item, index) => {
    const withDivider = index !== posetResults.length - 1;

    const buttonOnClick = () => {
      if (index !== activeButtonIndex) {
        setActiveButtonIndex(index);
      } else {
        setActiveButtonIndex(-1);
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
            // change button state to shown, clear other buttons
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
