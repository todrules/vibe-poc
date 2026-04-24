import type {
  GenerateRequestPayload,
  GenerateResponsePayload,
} from "@/types/generation";

function getApiBaseUrl(): string {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();
  if (baseUrl) {
    return baseUrl.replace(/\/$/, "");
  }

  // In production, route through the same origin (ALB listener rules route /generate to backend).
  // For local development, keep the previous localhost backend default.
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    if (hostname === "localhost" || hostname === "127.0.0.1") {
      return "http://127.0.0.1:8000";
    }
  }

  return "";
}

export async function generateArtifacts(
  payload: GenerateRequestPayload,
): Promise<GenerateResponsePayload> {
  const response = await fetch(`${getApiBaseUrl()}/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let detail = "Request failed.";

    try {
      const errorBody: unknown = await response.json();
      if (
        typeof errorBody === "object" &&
        errorBody !== null &&
        "detail" in errorBody &&
        typeof errorBody.detail === "string"
      ) {
        detail = errorBody.detail;
      }
    } catch {
      // Ignore JSON parse failures and fall back to generic detail.
    }

    throw new Error(`Generate request failed (${response.status}): ${detail}`);
  }

  return (await response.json()) as GenerateResponsePayload;
}
