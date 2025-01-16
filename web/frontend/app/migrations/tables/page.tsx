'use client'

import Link from "next/link";
import AppLayout from "@/components/layouts/AppLayout";
import {buttonVariants} from "@/components/ui/button"
import ListMigrationTable from "@/components/migrations/tables";
import React from "react";

export default function About() {
    return (
        <AppLayout
            breadcrumbItems={[
                {label: "Migrations", href: "/"},
                {label: "Tables"},
            ]}

            rightSection={
                <Link className={buttonVariants({variant: "outline"})} href={"/migrations/tables/add"}>Add Job</Link>
            }
        >
            <div>
                <ListMigrationTable className="mt-2" />
            </div>

        </AppLayout>
    );
}
