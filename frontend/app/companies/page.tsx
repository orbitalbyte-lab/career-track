export const dynamic = "force-dynamic";

import Link from "next/link";

import { serverApiFetch } from "../../lib/server-api";
import NewCompanyButton from "../../components/NewCompanyButton";
import EditCompanyButton from "../../components/EditCompanyButton";
import DeleteCompanyButton from "../../components/DeleteCompanyButton";

type Company = {
  id: number;
  name: string;
  website: string | null;
  industry: string | null;
  location: string | null;
  notes: string | null;
};

export default async function CompaniesPage() {
  let companies: Company[] = [];

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
              Companies
            </h1>

            <p className="mt-2 text-slate-500">
              Manage the companies connected to your applications.
            </p>
          </div>

          <NewCompanyButton />
        </div>

        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">Your Companies</h2>
              <p className="mt-1 text-sm text-slate-500">
                {companies.length}{" "}
                {companies.length === 1 ? "company" : "companies"}
              </p>
            </div>
          </div>

          <div className="mt-6 space-y-3">
            {companies.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-300 p-10 text-center">
                <h3 className="font-semibold">No companies yet</h3>
                <p className="mt-2 text-sm text-slate-500">
                  Add your first company to start organizing your applications.
                </p>
              </div>
            ) : (
              companies.map((company) => (
                <div
                  key={company.id}
                  className="rounded-xl border border-slate-200 p-5 transition hover:bg-slate-50"
                >
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                      <h3 className="font-semibold">{company.name}</h3>

                      <div className="mt-2 space-y-1 text-sm text-slate-500">
                        {company.industry && <p>{company.industry}</p>}

                        {company.location && <p>{company.location}</p>}

                        {company.website && (
                          <p className="break-all">{company.website}</p>
                        )}
                      </div>

                      {company.notes && (
                        <p className="mt-3 text-sm text-slate-600">
                          {company.notes}
                        </p>
                      )}
                    </div>

                    <div className="flex shrink-0 items-center gap-2">
                      <EditCompanyButton
                        companyId={company.id}
                        currentName={company.name}
                        currentWebsite={company.website}
                        currentIndustry={company.industry}
                        currentLocation={company.location}
                        currentNotes={company.notes}
                    />

                    <DeleteCompanyButton companyId={company.id} />

                    <span className="w-fit rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700">
                      Company #{company.id}
                    </span>
                   </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </div>
    </main>
  );
}