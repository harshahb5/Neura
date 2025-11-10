import axios from "axios";

// Point to backend; override with VITE_API_BASE in production if needed
const API_BASE = import.meta.env.VITE_API_BASE || "";

export const api = axios.create({
  baseURL: API_BASE,
});
