import { GraphData, PosetCoverResultData } from "../types";
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

const getAtgGraphData = async (
  size: number,
  selectedNodes: string[] | null = null,
  highlightedNodes: string[] | null = null
): Promise<GraphData> => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const params: Record<string, any> = { size };

  if (selectedNodes !== null) {
    params.selected_nodes = selectedNodes;
  }
  if (highlightedNodes !== null) {
    params.highlighted_nodes = highlightedNodes;
  }

  const response = await api.get(`/graph`, {
    params,
    paramsSerializer: {
      indexes: null,
    },
  });

  const parsedData: GraphData = JSON.parse(response.data);
  return parsedData;
};

const solveOptimalKPosetCover = async (
  k: number,
  upsilon: string[]
): Promise<PosetCoverResultData | null> => {
  const response = await api.get(`/solve`, {
    params: {
      k: k,
      upsilon: upsilon,
    },
    paramsSerializer: {
      indexes: null,
    },
  });

  const parsedData: PosetCoverResultData = JSON.parse(response.data);
  return Object.keys(parsedData).length !== 0 ? parsedData : null;
};

export default {
  getAtgGraphData,
  solveOptimalKPosetCover,
};
