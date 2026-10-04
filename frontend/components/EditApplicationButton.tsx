"use client";

import { useState } from "react";

type EditApplicationButtonProps = {
  applicationId: number;
};

export default function EditApplicationButton({
  applicationId,
}: EditApplicationButtonProps) {
  const [loading, setLoading] = useState(false);

  async function handleEdit() {
    setLoading(true);

    try {
      const response = await fetch(`/api/applications/${applicationId}`);

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to load application.");
      }

      const application = await response.json();

      const position = window.prompt(
        "Position:",
        application.position ?? "",
      );

      if (position === null) {
        return;
      }

      const status = window.prompt(
        "Status:",
        application.status ?? "Applied",
      );

      if (status === null) {
        return;
      }

      const responseUpdate = await fetch(
        `/api/applications/${applicationId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            position,
            status,
          }),
        },
      );

      if (!responseUpdate.ok) {
        const data = await responseUpdate.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to update application.");
      }

      window.location.reload();
    } catch (error) {
      alert(
        error instanceof Error
          ? error.message
          : "Failed to update application.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <button
      type="button"
      onClick={handleEdit}
      disabled={loading}
      className="w-fit rounded-xl border border-slate-300 px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {loading ? "Loading..." : "Edit"}
    </button>
  );
}