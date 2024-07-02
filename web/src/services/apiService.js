import axios from "axios";
import router from "@/router"; // Import your Vue Router instance
import { useAuthStore } from "@/store/authStore";

const instance = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
});

export const setAuthToken = () => {
  const authStore = useAuthStore();
  const tokenValue = authStore.accessToken;

  if (tokenValue) {
    instance.defaults.headers.common["Authorization"] = `Bearer ${tokenValue}`;
  } else {
    delete instance.defaults.headers.common["Authorization"];
  }
};

// Axios interceptor to handle token expiration
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response.status === 401) {
      const isTokenExpired = isExpiredToken();

      if (isTokenExpired) {
        router.push("/");
      }
    }
    return Promise.reject(error);
  }
);

// Function to check if the token is expired
const isExpiredToken = () => {
  const authStore = useAuthStore();
  const tokenValue = authStore.accessToken;

  if (!tokenValue) {
    return false; // Token is missing, consider it expired
  }

  const decodedToken = parseJwt(tokenValue);
  const expirationTime = decodedToken.exp * 1000; // Convert to milliseconds

  return Date.now() >= expirationTime;
};

// Function to parse JWT tokens
const parseJwt = (token) => {
  const base64Url = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  return JSON.parse(jsonPayload);
};

export const fetchData = async (url, nextPage = 0, limit = "", search = "") => {
  const response = await instance.get(
    `/${url}?skip=${nextPage}&limit=${limit}&search=${search}`
  );
  return response.data;
};

export const fetchItem = async (url, itemId) => {
  const response = await instance.get(`/${url}/${itemId}`);
  return response.data;
};

export const createItem = async (url, itemData) => {
  const response = await instance.post(`/${url}`, itemData);
  return response.data;
};

export const updateItem = async (url, itemId, updatedData) => {
  const response = await instance.put(`/${url}/${itemId}`, updatedData);
  return response.data;
};

export const deleteItem = async (url, itemId) => {
  const response = await instance.delete(`/${url}/${itemId}`);
  return response.data;
};

export const logout = async (url) => {
  const response = await instance.post(`/${url}`);
  return response.data;
};

// Update your fetchItem function
export const downloadItem = async (url, itemId) => {
  const response = await instance.get(`/${url}/${itemId}`, {
    responseType: "blob", // Set responseType to 'blob'
  });
  return response;
};
