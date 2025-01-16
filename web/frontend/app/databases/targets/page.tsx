'use client'

import Link from "next/link";
import AppLayout from "@/components/layouts/AppLayout";
import {buttonVariants} from "@/components/ui/button"
import ListDatabase from "@/components/databases/list";
import React from "react";

export default function About() {
    return (
        <AppLayout
            breadcrumbItems={[
                {label: "Databases", href: "/"},
                {label: "Targets"},
            ]}

            rightSection={
                <Link className={buttonVariants({variant: "outline"})} href={"/databases/targets/add"}>Add Target</Link>
            }
        >
            <div>
                <ListDatabase className="mt-2" type="target" />
            </div>

        </AppLayout>
    );
}
