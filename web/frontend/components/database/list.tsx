import { useEffect, useState, useRef } from "react";
import { cn } from "@/lib/utils";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

interface Database {
    id: number;
    name: string;
    host: string;
    port: number;
    user: string;
    type: string;
    status: string;
    created_at: string;
    updated_at: string;
}

export default function ListDatabase({
                                         className,
                                         ...props
                                     }: React.ComponentPropsWithoutRef<"div">) {
    const [databases, setDatabases] = useState<Database[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const isFetched = useRef(false); // Prevent double fetch

    useEffect(() => {
        const fetchDatabases = async () => {
            try {
                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_API_BASE_URL}/databases/list`
                );
                if (!response.ok) {
                    throw new Error("Failed to fetch databases");
                }
                const data = await response.json();
                console.log("API Response:", data); // Log the response
                setDatabases(data.data || []);
            } catch (error) {
                console.error("Error fetching databases:", error);
            } finally {
                setLoading(false);
            }
        };

        if (!isFetched.current) {
            isFetched.current = true; // Mark as fetched
            fetchDatabases();
        }
    }, []);

    if (loading) {
        return <p>Loading databases...</p>;
    }

    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Table>
                <TableCaption>A list of your recent databases.</TableCaption>
                <TableHeader>
                    <TableRow>
                        <TableHead className="w-[100px]">ID</TableHead>
                        <TableHead>Name</TableHead>
                        <TableHead>Host</TableHead>
                        <TableHead>Port</TableHead>
                        <TableHead>User</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Created At</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {databases.map((db) => (
                        <TableRow key={db.id}>
                            <TableCell className="font-medium">{db.id}</TableCell>
                            <TableCell>{db.name}</TableCell>
                            <TableCell>{db.host}</TableCell>
                            <TableCell>{db.port}</TableCell>
                            <TableCell>{db.user}</TableCell>
                            <TableCell>{db.type}</TableCell>
                            <TableCell>{db.status}</TableCell>
                            <TableCell>{new Date(db.created_at).toLocaleString()}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
}
