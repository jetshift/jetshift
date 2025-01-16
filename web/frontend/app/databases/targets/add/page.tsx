'use client'

import AppLayout from "@/components/layouts/AppLayout";
import AddDatabase from "@/components/database/add-database";

export default function About() {
    return (
        <AppLayout
            breadcrumbItems={[
                {label: "Databases", href: "/"},
                {label: "Targets", href: "/databases/targets"},
                {label: "Add"},
            ]}
        >
            <div className="flex flex-col items-center justify-center gap-6 bg-muted p-6 md:p-10">
                <div className="flex w-full max-w-lg flex-col gap-6">
                    <AddDatabase type="target"/>
                </div>
            </div>

        </AppLayout>
    );
}
