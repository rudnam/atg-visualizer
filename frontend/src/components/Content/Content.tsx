import React, { useState } from "react";
import InputForm from "../InputForm/InputForm";
import Graph from "../Graph/Graph";
import { GraphData, PosetResult } from "../../types";
import ResultsPanel from "../ResultsPanel/ResultsPanel";
import posetService from "../../services/poset";

const Content: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [atgGraph, setAtgGraph] = useState<GraphData | null>(null);
  const [posetResults, setPosetResults] = useState<PosetResult[]>([]);
  const [highlightedPosetIndex, setHighlightedPosetIndex] =
    useState<number>(-1);

  const fetchEntireGraphData = async (size: number, upsilon: string[]) => {
    try {
      if (upsilon.length > 0 && size !== upsilon[0].length) {
        throw new Error(
          `Indicated permutation length (Slider: ${size}) is not equal to length of given permutations, e.g. '${upsilon[0]}'.`
        );
      }
      setLoading(true);
      setPosetResults([]);
      setHighlightedPosetIndex(-1);

      const atgGraphData = await posetService.getAtgGraphData(size);
      setAtgGraph(atgGraphData);
    } catch (error) {
      console.error("Error rendering the plot:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPosetCoverResults = async (
    size: number,
    k: number,
    upsilon: string[]
  ) => {
    try {
      if (upsilon.length > 0 && size !== upsilon[0].length) {
        throw new Error(
          `Indicated permutation length (Slider: ${size}) is not equal to length of given permutations, e.g. '${upsilon[0]}'.`
        );
      }
      setLoading(true);
      setPosetResults([]);
      setHighlightedPosetIndex(-1);

      const posetCoverResultData = await posetService.solveOptimalKPosetCover(
        k,
        upsilon
      );

      if (posetCoverResultData !== null) {
        const resultLinearOrders = posetCoverResultData.resultLinearOrders;
        const resultPosets = posetCoverResultData.resultPosets;

        const resolvedResults = await Promise.all(
          resultLinearOrders.map(async (result, index) => {
            const posetGraphData = await posetService.getAtgGraphData(
              size,
              upsilon,
              result
            );
            return {
              name: `P${index + 1}`,
              relations: resultPosets[index],
              linearExtensions: result,
              graphData: posetGraphData,
            };
          })
        );

        setPosetResults(resolvedResults);
      } else {
        alert("No result found.");
      }
    } catch (error) {
      console.error("Error rendering the plot:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full px-4 md:px-8 grow flex flex-col sm:flex-row justify-center gap-12 w-full max-w-6xl mx-auto">
      <InputForm
        fetchEntireGraphData={fetchEntireGraphData}
        fetchPosetCoverResults={fetchPosetCoverResults}
        loading={loading}
      />
      <Graph
        loading={loading}
        graphData={
          highlightedPosetIndex === -1
            ? atgGraph
            : posetResults[highlightedPosetIndex]?.graphData || null
        }
      />
      <ResultsPanel
        posetResults={posetResults}
        highlightedPosetIndex={highlightedPosetIndex}
        setHighlightedPosetIndex={setHighlightedPosetIndex}
      />
    </div>
  );
};

export default Content;
