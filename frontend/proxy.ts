import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const accessToken = request.cookies.get("access_token")?.value;

  if (!accessToken) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/",
    "/applications/:path*",
    "/companies/:path*",
    "/interviews/:path*",
    "/follow-ups/:path*",
    "/analytics/:path*",
  ],
};
