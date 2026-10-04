export const dynamic = "force-dynamic";

import Link from "next/link";

import { serverApiFetch } from "../../lib/server-api";
import NewApplicationButton from "../../components/NewApplicationButton";
import EditApplicationButton from "../../components/EditApplicationButton";
import DeleteApplicationButton from "../../components/DeleteApplicationButton";

type Application = {
  id: number;
  company_id: number;
  position: string;
  application_type: string;
  date_applied: string;
  status: string;
  location: string | null;
  deadline: string | null;
  job_url: string | null;
  notes: string | null;
};

type Company = {
  id: number;
  name: string;
};

export default async function ApplicationsPage() {
  let applications: Application[] = [];
  let companies: Company[] = [];

  try {
    applications = await serverApiFetch<Application[]>("/api/applications");
  } catch {
    applications = [];
  }

  try {
    companies = await serverApiFetch<Company[]>("/api/companies");
  } catch {
    companies = [];
  }

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-8 text-slate-950 lg:px-10">
      <div className="mx-auto max-w-6xl">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <Link
              href="/"
              className="text-sm font-medium text-slate-500 hover:text-slate-950"
            >
              ← Dashboard
            </Link>

            <h1 className="mt-3 text-3xl font-bold tracking-tight">
              Applications
            </h1>

            <p className="mt-2 text-slate-500">
              Track all your job and internship applications.
            </p>
          </div>

          <NewApplicationButton companies={companies} />
        </div>

        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div>
            <h2 className="text-lg font-semibold">Your Applications</h2>
            <p className="mt-1 text-sm text-slate-500">
              {applications.length}{" "}
              {applications.length === 1 ? "application" : "applications"}
            </p>
          </div>

          <div className="mt-6 space-y-3">
            {applications.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-300 p-10 text-center">
                <h3 className="font-semibold">No applications yet</h3>
                <p className="mt-2 text-sm text-slate-500">
                  Add your first application from the dashboard.
                </p>
              </div>
            ) : (
              applications.map((application) => {
                const company = companies.find(
                  (item) => item.id === application.company_id,
                );

                return (
                  <div
                    key={application.id}
                    className="rounded-xl border border-slate-200 p-5 transition hover:bg-slate-50"
                  >
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                      <div className="min-w-0">
                        <h3 className="font-semibold">
                          {application.position}
                        </h3>

                        <p className="mt-1 text-sm text-slate-500">
                          {company?.name ?? "Company not found"}
                        </p>

                        <div className="mt-3 grid gap-2 text-sm text-slate-500 sm:grid-cols-2">
                          <p>
                            <span className="font-medium text-slate-700">
                              Type:
                            </span>{" "}
                            {application.application_type}
                          </p>

                          <p>
                            <span className="font-medium text-slate-700">
                              Applied:
                            </span>{" "}
                            {application.date_applied}
                          </p>

                          <p>
                            <span className="font-medium text-slate-700">
                              Location:
                            </span>{" "}
                            {application.location ?? "Not specified"}
                          </p>

                          <p>
                            <span className="font-medium text-slate-700">
                              Deadline:
                            </span>{" "}
                            {application.deadline ?? "Not specified"}
                          </p>
                        </div>

                        {application.job_url && (
                          <p className="mt-3 break-all text-sm text-slate-500">
                            <span className="font-medium text-slate-700">
                              Job URL:
                            </span>{" "}
                            {application.job_url}
                          </p>
                        )}

                        {application.notes && (
                          <p className="mt-3 text-sm text-slate-600">
                            {application.notes}
                          </p>
                        )}
                      </div>

                      <div className="flex shrink-0 flex-col items-end gap-2">
                        <span className="w-fit rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700">
                          {application.status}
                        </span>

                        <div className="flex gap-2">
                          <EditApplicationButton
                            applicationId={application.id}
                          />

                          <DeleteApplicationButton
                            applicationId={application.id}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </section>
      </div>
    </main>
  );
}