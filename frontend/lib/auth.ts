import { apiFetch } from "./api";

type LoginResponse = {
  access_token: string;
  token_type: string;
};

export async function login(email: string, password: string) {
  return apiFetch<LoginResponse>("/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });
}