import { cookies } from "next/headers";
import { NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type RouteContext = {
  params: Promise<{
    id: string;
  }>;
};

export async function GET(
  request: Request,
  { params }: RouteContext,
) {
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

  const { id } = await params;

  const response = await fetch(`${API_URL}/api/interviews/${id}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    cache: "no-store",
  });

  const data = await response.json().catch(() => null);

  return NextResponse.json(data, { status: response.status });
}

export async function PUT(
  request: Request,
  { params }: RouteContext,
) {
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

  const { id } = await params;
  const body = await request.json();

  const response = await fetch(`${API_URL}/api/interviews/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(body),
  });

  const data = await response.json().catch(() => null);

  return NextResponse.json(data, { status: response.status });
}

export async function DELETE(
  request: Request,
  { params }: RouteContext,
) {
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

  const { id } = await params;

  const response = await fetch(`${API_URL}/api/interviews/${id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);

    return NextResponse.json(
      data ?? { detail: "Failed to delete interview." },
      { status: response.status },
    );
  }

  return new NextResponse(null, { status: 204 });
}
