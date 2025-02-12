import React, { useState } from "react";
import InputForm from "./InputForm";
import Graph from "./Graph";
import { GraphData, PosetResult } from "../types";
import ResultsPanel from "./ResultsPanel";
import poset from "../services/poset";

const Content: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [atgGraph, setAtgGraph] = useState<GraphData | null>(null);
  const [lastDrawRequestUpsilon, setLastDrawRequestUpsilon] = useState<
    string[]
  >([]);
  const [lastSolveRequestUpsilon, setLastSolveRequestUpsilon] = useState<
    string[]
  >([]);
  const [posetResults, setPosetResults] = useState<PosetResult[]>([]);
  const [highlightedPosetIndex, setHighlightedPosetIndex] =
    useState<number>(-1);

  const fetchEntireGraphData = async (size: number, upsilon: string[]) => {
    try {
      if (size !== upsilon[0].length) {
        throw new Error(
          `Indicated permutation length (Slider: ${size}) is not equal to length of given permutations, e.g. '${upsilon[0]}'.`
        );
      }
      setLoading(true);
      setPosetResults([]);
      setHighlightedPosetIndex(-1);
      const atgGraphData = await poset.getAtgGraphData(size, upsilon);
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
      if (size !== upsilon[0].length) {
        throw new Error(
          `Indicated permutation length (Slider: ${size}) is not equal to length of given permutations, e.g. '${upsilon[0]}'.`
        );
      }
      setLoading(true);
      setPosetResults([]);
      setHighlightedPosetIndex(-1);

      const posetCoverResultData = await poset.solveOptimalKPosetCover(
        k,
        upsilon
      );

      if (posetCoverResultData !== null) {
        const resultLinearOrders = posetCoverResultData.resultLinearOrders;
        const resultPosets = posetCoverResultData.resultPosets;

        const resolvedResults = await Promise.all(
          resultLinearOrders.map(async (result, index) => {
            const posetGraphData = await poset.getAtgGraphData(
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

  const onClickDrawButton = async (size: number, upsilon: string[]) => {
    const isNewRequest =
      lastDrawRequestUpsilon.length === 0 ||
      !lastDrawRequestUpsilon.every((val, idx) => upsilon[idx] === val);
    if (!isNewRequest) {
      alert("The ATG for this input has already been drawn.");
      return;
    }
    setLastDrawRequestUpsilon(upsilon);
    await fetchEntireGraphData(size, upsilon);
  };

  const onClickSolveButton = async (
    size: number,
    k: number,
    upsilon: string[]
  ) => {
    const isNewSolveRequest =
      lastSolveRequestUpsilon.length === 0 ||
      !lastSolveRequestUpsilon.every((val, idx) => upsilon[idx] === val);
    if (!isNewSolveRequest) {
      alert("The solution for this input graph has already been computed.");
      return;
    }
    const hasntBeenDrawnYet =
      lastDrawRequestUpsilon.length === 0 ||
      !lastDrawRequestUpsilon.every((val, idx) => upsilon[idx] === val);

    if (hasntBeenDrawnYet) {
      setLastDrawRequestUpsilon(upsilon);
      await fetchEntireGraphData(size, upsilon);
    }

    setLastSolveRequestUpsilon(upsilon);
    await fetchPosetCoverResults(size, k, upsilon);
  };

  return (
    <div className="h-full px-4 md:px-8 grow flex flex-col sm:flex-row justify-center gap-12 w-full max-w-6xl mx-auto">
      <InputForm
        onClickDrawButton={onClickDrawButton}
        onClickSolveButton={onClickSolveButton}
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
