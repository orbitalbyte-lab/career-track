const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not configured.");
}

export async function apiFetch<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_URL}${path}`, options);
  } catch {
    throw new Error(
      "Unable to connect to the server. Please make sure CareerTrack is running.",
    );
  }

  if (!response.ok) {
    const data = await response.json().catch(() => null);

    const detail =
      data && typeof data.detail === "string"
        ? data.detail
        : `API request failed: ${response.status}`;

    throw new Error(detail);
  }

  return response.json();
}