"use client";

import { useState } from "react";

type DeleteApplicationButtonProps = {
  applicationId: number;
};

export default function DeleteApplicationButton({
  applicationId,
}: DeleteApplicationButtonProps) {
  const [loading, setLoading] = useState(false);

  async function handleDelete() {
    const confirmed = window.confirm(
      "Are you sure you want to delete this application?",
    );

    if (!confirmed) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`/api/applications/${applicationId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to delete application.");
      }

      window.location.reload();
    } catch (error) {
      alert(
        error instanceof Error
          ? error.message
          : "Failed to delete application.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <button
      type="button"
      onClick={handleDelete}
      disabled={loading}
      className="w-fit rounded-xl border border-red-200 px-3 py-2 text-xs font-semibold text-red-600 transition hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {loading ? "Deleting..." : "Delete"}
    </button>
  );
}