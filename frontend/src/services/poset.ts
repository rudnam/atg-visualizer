import {
  DrawingMethod,
  GraphData,
  PosetCoverResultData,
  Relation,
} from "../types";
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

const getAtgGraphData = async (
  size: number,
  drawingMethod: DrawingMethod,
  selectedNodes: string[] | null = null,
  highlightedNodes: string[] | null = null,
): Promise<GraphData> => {
  const response = await api.post(`/graph`, {
    input_mode: "Linear Orders",
    drawing_method: drawingMethod,
    size,
    selected_nodes: selectedNodes ?? [],
    highlighted_nodes: highlightedNodes ?? [],
  });

  const parsedData: GraphData = JSON.parse(response.data);
  return parsedData;
};

const getAtgGraphDataFromCoverRelation = async (
  size: number,
  drawingMethod: DrawingMethod,
  coverRelation: Relation[],
): Promise<GraphData> => {
  try {
    const response = await api.post(`/graph`, {
      input_mode: "Poset",
      drawing_method: drawingMethod,
      size,
      cover_relation: coverRelation ?? [],
    });

    const parsedData: GraphData = JSON.parse(response.data);
    return parsedData;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverMessage = error.response?.data?.detail || error.message;

      throw new Error(`${serverMessage}`);
    } else {
      throw new Error(`Unexpected error: ${error}`);
    }
  }
};

const solveOptimalKPosetCover = async (
  k: number,
  upsilon: string[],
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
  getAtgGraphDataFromCoverRelation,
  solveOptimalKPosetCover,
};
