import axios from "axios";

// 👇 Replace this URL with your Render backend URL
const API_BASE = "https://neura-flzk.onrender.com";

export const api = axios.create({
  baseURL: API_BASE,
});
