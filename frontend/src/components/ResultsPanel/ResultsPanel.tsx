import { ScrollArea } from "@mantine/core";
import React from "react";
import { PosetResult } from "../../types";
import PosetResultComponent from "./PosetResultComponent";

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
  return (
    <div className="h-full w-72 max-h-[36rem] mx-auto md:mx-0 gap-4 bg-[#fefefe] p-8 rounded-xl shadow-lg">
      <div className="text-xl font-bold">RESULTS</div>
      <ScrollArea scrollbarSize={4} offsetScrollbars className="h-full py-4">
        {posetResults.map((posetResult, index) => (
          <PosetResultComponent
            name={posetResult.name}
            linearExtensions={posetResult.linearExtensions}
            withDivider={index !== posetResults.length - 1}
            buttonVariant={
              index === highlightedPosetIndex ? "filled" : "outline"
            }
            buttonOnClick={() => {
              if (index === highlightedPosetIndex) {
                setHighlightedPosetIndex(-1);
              } else {
                setHighlightedPosetIndex(index);
              }
            }}
          />
        ))}
      </ScrollArea>
    </div>
  );
};

export default ResultsPanel;
