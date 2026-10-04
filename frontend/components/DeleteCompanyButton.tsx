"use client";

import { useState } from "react";

type DeleteCompanyButtonProps = {
  companyId: number;
};

export default function DeleteCompanyButton({
  companyId,
}: DeleteCompanyButtonProps) {
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");

  async function handleDelete() {
    const confirmed = window.confirm(
      "Are you sure you want to delete this company?",
    );

    if (!confirmed) {
      return;
    }

    setDeleting(true);
    setError("");

    try {
      const response = await fetch(`/api/companies/${companyId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);

        throw new Error(
          data?.detail ?? `Failed to delete company: ${response.status}`,
        );
      }

      window.location.reload();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to delete company.",
      );
      setDeleting(false);
    }
  }

  return (
    <div>
      <button
        type="button"
        onClick={handleDelete}
        disabled={deleting}
        className="rounded-lg border border-red-200 px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50 disabled:opacity-50"
      >
        {deleting ? "Deleting..." : "Delete"}
      </button>

      {error && (
        <p className="mt-2 text-xs text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}