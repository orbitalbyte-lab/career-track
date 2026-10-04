import { NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type LoginResponse = {
  access_token: string;
  token_type: string;
};

export async function POST(request: Request) {
  if (!API_URL) {
    return NextResponse.json(
      { detail: "NEXT_PUBLIC_API_URL is not configured." },
      { status: 500 },
    );
  }

  const body = await request.json();

  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  const data = (await response.json()) as LoginResponse | { detail?: string };

  if (!response.ok) {
    return NextResponse.json(data, { status: response.status });
  }

  const tokenData = data as LoginResponse;

  const nextResponse = NextResponse.json({
    token_type: tokenData.token_type,
  });

  nextResponse.cookies.set("access_token", tokenData.access_token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 30,
  });

  return nextResponse;
}