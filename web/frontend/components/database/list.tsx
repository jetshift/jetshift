import {useEffect, useState, useRef} from "react";
import {cn} from "@/lib/utils";
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
    type: string;
    name: string;
    host: string;
    port: number;
    user: string;
    database: string;
    engine: string;
    status: boolean;
    created_at: string;
    updated_at: string;
}

interface ListDatabaseProps extends React.ComponentPropsWithoutRef<"div"> {
    type?: string;
}

export default function ListDatabase(
    {
        className,
        type, // Destructure 'type' from props
        ...props
    }: ListDatabaseProps) {

    const [databases, setDatabases] = useState<Database[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const isFetched = useRef(false); // Prevent double fetch

    useEffect(() => {
        const fetchDatabases = async () => {
            try {
                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_API_BASE_URL}/databases/list${type ? `?type=${type}` : ''}`
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
    }, [type]); // Include 'type' in the dependency array

    if (loading) {
        return <p>Loading databases...</p>;
    }

    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Table>
                <TableCaption className="hidden">A list of your recent databases.</TableCaption>
                <TableHeader>
                    <TableRow>
                        <TableHead className="w-[100px]">ID</TableHead>
                        <TableHead>Name</TableHead>
                        <TableHead>Engine</TableHead>
                        <TableHead>Host</TableHead>
                        <TableHead>Port</TableHead>
                        <TableHead>User</TableHead>
                        <TableHead>Database</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Created At</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {databases.map((db) => (
                        <TableRow key={db.id}>
                            <TableCell className="font-medium">{db.id}</TableCell>
                            <TableCell>{db.name}</TableCell>
                            <TableCell>{db.engine}</TableCell>
                            <TableCell>{db.host}</TableCell>
                            <TableCell>{db.port}</TableCell>
                            <TableCell>{db.user}</TableCell>
                            <TableCell>{db.database}</TableCell>
                            <TableCell>{db.status == 1 ? 'Active' : 'Inactive'}</TableCell>
                            <TableCell>{new Date(db.created_at).toLocaleString()}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
}
