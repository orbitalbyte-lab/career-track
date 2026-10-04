"use client";

import { useState } from "react";

type DeleteFollowUpButtonProps = {
  followUpId: number;
};

export default function DeleteFollowUpButton({
  followUpId,
}: DeleteFollowUpButtonProps) {
  const [loading, setLoading] = useState(false);

  async function handleDelete() {
    const confirmed = window.confirm(
      "Are you sure you want to delete this follow-up?",
    );

    if (!confirmed) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`/api/follow-ups/${followUpId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to delete follow-up.");
      }

      window.location.reload();
    } catch (error) {
      alert(
        error instanceof Error
          ? error.message
          : "Failed to delete follow-up.",
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