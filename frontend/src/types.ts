import { Layout } from "plotly.js-dist";

export interface GraphData {
  data: Plotly.Data[];
  layout: Partial<Layout>;
}

export type InputMode = "Linear Orders" | "Poset";

export type DrawingMethod =
  | "Default"
  | "Permutahedron"
  | "Supercover"
  | "Hexagonal"
  | "Supercover + Hexagonal"
  | "Hexagonal1"
  | "Supercover + Hexagonal 1";

export type Relation = [number, number];

export interface PosetCoverResultData {
  resultPosets: Relation[][];
  resultLinearOrders: string[][];
}

export interface PosetResult {
  name: string;
  relations: Relation[];
  linearExtensions: string[];
  graphData?: GraphData;
}
