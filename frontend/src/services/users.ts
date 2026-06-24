import api from "./api";

export const signupUser = async (
  name: string,
  email: string,
  password: string,
  role: string
) => {
  const response = await api.post("/signup", {
    name,
    email,
    password,
    role,
  });

  return response.data;
};