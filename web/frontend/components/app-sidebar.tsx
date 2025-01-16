"use client"

import * as React from "react"
import {
    Database,
    LayoutDashboard,
    FolderSync
} from "lucide-react"

import {NavMain} from "@/components/nav-main"
// import {NavProjects} from "@/components/nav-projects"
import {NavUser} from "@/components/nav-user"
// import {TeamSwitcher} from "@/components/team-switcher"
import {NavJetShift} from "@/components/nav-jetshift";
import {
    SidebarGroup,
    Sidebar,
    SidebarContent,
    SidebarMenu,
    SidebarFooter,
    SidebarHeader, SidebarMenuButton, SidebarMenuItem,
    SidebarRail,
} from "@/components/ui/sidebar"

import Link from 'next/link'

// Data
const data = {
    user: {
        name: "shadcn",
        email: "m@example.com",
        avatar: "/",
        // avatar: "/avatars/shadcn.jpg",
    },
    navMain: [
        {
            title: "Databases",
            url: "#",
            icon: Database,
            isActive: true,
            items: [
                {
                    title: "Sources",
                    url: "/databases/sources",
                },
                {
                    title: "Targets",
                    url: "/databases/targets",
                },
            ],
        },
        {
            title: "Migrations",
            url: "#",
            icon: FolderSync,
            isActive: true,
            items: [
                {
                    title: "Databases",
                    url: "/migrations/databases",
                },
                {
                    title: "Tables",
                    url: "/migrations/tables",
                },
            ],
        },
    ],
    // projects: [
    //     {
    //         name: "Design Engineering",
    //         url: "#",
    //         icon: Frame,
    //     },
    //     {
    //         name: "Sales & Marketing",
    //         url: "#",
    //         icon: PieChart,
    //     },
    //     {
    //         name: "Travel",
    //         url: "#",
    //         icon: Map,
    //     },
    // ],
}

export function AppSidebar({...props}: React.ComponentProps<typeof Sidebar>) {
    return (
        <Sidebar collapsible="icon" {...props}>
            <SidebarHeader>
                <NavJetShift/>
            </SidebarHeader>
            <SidebarContent>

                {/* Dashboard */}
                <SidebarGroup className="group-data-[collapsible=icon]:hidden">
                    <SidebarMenu>
                        <SidebarMenuItem>
                            <Link href="/">
                                <SidebarMenuButton tooltip='sss'>
                                    <LayoutDashboard/>
                                    <span>Dashboard</span>
                                </SidebarMenuButton>
                            </Link>
                        </SidebarMenuItem>
                    </SidebarMenu>
                </SidebarGroup>

                <NavMain items={data.navMain}/>
                {/*<NavProjects projects={data.projects}/>*/}
            </SidebarContent>
            <SidebarFooter>
                <NavUser user={data.user}/>
            </SidebarFooter>
            <SidebarRail/>
        </Sidebar>
    )
}
