'use client'

import AppLayout from "@/components/layouts/AppLayout";
import AddDatabase from "@/components/database/add-database";

export default function About() {
    return (
        <AppLayout
            breadcrumbItems={[
                {label: "Databases", href: "/"},
                {label: "Sources", href: "/databases/sources"},
                {label: "Add"},
            ]}
        >
            <div className="flex flex-col items-center justify-center gap-6 bg-muted p-6 md:p-10">
                <div className="flex w-full max-w-lg flex-col gap-6">
                    <AddDatabase type="source"/>
                </div>
            </div>

        </AppLayout>
    );
}
