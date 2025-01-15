'use client'

import Link from "next/link";
import AppLayout from "@/components/layouts/AppLayout";
import {buttonVariants} from "@/components/ui/button"
import ListDatabase from "@/components/database/list";
import React from "react";

export default function About() {
    return (
        <AppLayout
            breadcrumbItems={[
                {label: "Databases", href: "/"},
                {label: "Sources"},
            ]}

            rightSection={
                <Link className={buttonVariants({variant: "outline"})} href={"/databases/sources/add"}>Add Source</Link>
            }
        >
            <div>
                <ListDatabase className="mt-2" type="source" />
            </div>

        </AppLayout>
    );
}
