import React, { useState } from "react";
import InputForm from "./InputForm";
import Graph from "./Graph";
import api from "../api";
import { GraphData, PosetResult } from "../types";
import ResultsPanel from "./ResultsPanel";

const Content: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [graphData, setGraphData] = useState<GraphData[]>([]);
  const [atgGraph, setAtgGraph] = useState<GraphData | null>(null);
  const [posetResults, setPosetResults] = useState<PosetResult[]>([]);
  const [highlightedPosetIndex, setHighlightedPosetIndex] = useState<number>(-1);

  const fetchGraphData = async (size: number, k: number, upsilon: string[]) => {
    try {
      setGraphData([]);
      setLoading(true);
      setHighlightedPosetIndex(-1);

      const response = await api.get(`/solve`, {
        params: {
          k: k,
          upsilon: upsilon,
        },
        paramsSerializer: {
          indexes: null,
        },
      });

      const graphResponse = await api.get(`/graph`, {
        params: {
          size: size,
          selected_nodes: upsilon,
        },
        paramsSerializer: {
          indexes: null,
        },
      });

      const atgGraphData = JSON.parse(graphResponse.data);
      setAtgGraph(atgGraphData);
      
      const parsedData = JSON.parse(response.data);
      if (Object.keys(parsedData).length !== 0) {
        const resultLinearOrders: string[][] = parsedData.result_linear_orders;
        setPosetResults(
          resultLinearOrders.map((result, index) => ({
            name: `P${index + 1}`,
            linearExtensions: result,
          }))
        );

        for (const linearOrders of resultLinearOrders) {
          const graphResponse = await api.get(`/graph`, {
            params: {
              size: size,
              selected_nodes: upsilon,
              highlighted_nodes: linearOrders,
            },
            paramsSerializer: {
              indexes: null,
            },
          });

          const parsedGraphData = JSON.parse(graphResponse.data);
          setGraphData((data) => [...data, parsedGraphData]);
        }
      } else {
        alert("No result found.");
        setPosetResults([]);
        setGraphData([]);
      }
    } catch (error) {
      console.error("Error rendering the plot:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full px-4 md:px-8 grow flex flex-col sm:flex-row justify-center gap-12 w-full max-w-6xl mx-auto">
      <InputForm fetchGraphData={fetchGraphData} />
      <Graph
        loading={loading}
        graphData={
          highlightedPosetIndex===-1 ? atgGraph :
          graphData.length > 0 ? graphData[highlightedPosetIndex] : null}
      />
      <ResultsPanel posetResults={posetResults} highlightedPosetIndex={highlightedPosetIndex} setHighlightedPosetIndex={setHighlightedPosetIndex} />
    </div>
  );
};

export default Content;
