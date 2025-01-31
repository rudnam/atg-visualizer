import React, { useState } from "react";
import InputForm from "./InputForm";
import Graph from "./Graph";
import api from "../api";
import { GraphData, PosetResult } from "../types";
import ResultsPanel from "./ResultsPanel";

const Content: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [graphData, setGraphData] = useState<GraphData[]>([]);
  const [posetResults, setPosetResults] = useState<PosetResult[]>([]);
  const [graphIndex, setGraphIndex] = useState<number>(0);

  const fetchGraphData = async (size: number, k: number, upsilon: string[]) => {
    try {
      setGraphData([]);
      setLoading(true);

      const response = await api.get(`/solve`, {
        params: {
          k: k,
          upsilon: upsilon,
        },
        paramsSerializer: {
          indexes: null,
        },
      });

      const parsedData = JSON.parse(response.data);
      console.log(parsedData);

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
              selected_nodes: linearOrders,
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
        graphData={graphData.length > 0 ? graphData[graphIndex] : null}
      />
      <ResultsPanel posetResults={posetResults} setGraphIndex={setGraphIndex} />
    </div>
  );
};

export default Content;
