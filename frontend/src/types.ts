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
  | "SuperHex"

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
