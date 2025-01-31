import React, { useState } from "react";
import InputForm from "./InputForm";
import Graph from "./Graph";
import api from "../api";
import { GraphData } from "../types";

const Content: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [graphData, setGraphData] = useState<GraphData | null>(null);

  const fetchPlotData = async (size: number, selectedNodes: string[]) => {
    try {
      setGraphData(null);
      setLoading(true);

      const response = await api.get(`/graph`, {
        params: {
          size: size,
          selected_nodes: selectedNodes,
        },
        paramsSerializer: {
          indexes: null,
        },
      });

      const parsedData: GraphData = JSON.parse(response.data);

      setGraphData(parsedData);
    } catch (error) {
      console.error("Error rendering the plot:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full px-4 md:px-8 grow flex flex-col sm:flex-row justify-center gap-12 w-full max-w-6xl mx-auto">
      <InputForm fetchPlotData={fetchPlotData} />
      <Graph loading={loading} graphData={graphData} />
    </div>
  );
};

export default Content;
