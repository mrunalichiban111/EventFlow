import api from "./api";

export const loginUser = async (
  email: string,
  password: string
) => {
  const response = await api.post("/login", {
    email,
    password,
  });

  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get("/me");

  return response.data;
};