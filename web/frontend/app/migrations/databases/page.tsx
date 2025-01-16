'use client'

import Link from "next/link";
import AppLayout from "@/components/layouts/AppLayout";
import {buttonVariants} from "@/components/ui/button"
import ListMigrationDatabase from "@/components/migrations/databases";
import React from "react";

export default function About() {
    return (
        <AppLayout
            breadcrumbItems={[
                {label: "Migrations", href: "/"},
                {label: "Databases"},
            ]}

            rightSection={
                <Link className={buttonVariants({variant: "outline"})} href={"/migrations/databases/add"}>Add Job</Link>
            }
        >
            <div>
                <ListMigrationDatabase className="mt-2" />
            </div>

        </AppLayout>
    );
}
