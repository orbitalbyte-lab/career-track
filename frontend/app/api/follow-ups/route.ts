import { cookies } from "next/headers";
import { NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function POST(request: Request) {
  if (!API_URL) {
    return NextResponse.json(
      { detail: "NEXT_PUBLIC_API_URL is not configured." },
      { status: 500 },
    );
  }

  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  if (!accessToken) {
    return NextResponse.json(
      { detail: "Not authenticated." },
      { status: 401 },
    );
  }

  const body = await request.json();

  const response = await fetch(`${API_URL}/api/follow-ups`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(body),
  });

  const data = await response.json().catch(() => null);

  return NextResponse.json(data, { status: response.status });
}