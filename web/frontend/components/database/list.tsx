import {useEffect, useState, useRef} from "react";
import {cn} from "@/lib/utils";
import {Router} from "lucide-react";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import JSAlertDialog from "@/components/common/js-alert-dialog";

interface Database {
    id: number;
    type: string;
    name: string;
    host: string;
    port: number;
    username: string;
    database: string;
    dialect: string;
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
        type,
        ...props
    }: ListDatabaseProps) {

    const [databases, setDatabases] = useState<Database[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const isFetched = useRef(false);

    // JSAlertDialog
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");

    const checkConnection = async (id: number) => {
        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_BASE_URL}/databases/check-connection/${id}`,
                {
                    method: "GET",
                }
            );
            if (!response.ok) {
                throw new Error("Failed to check database connection");
            }
            const data = await response.json();

            setIsDialogOpen(true);
            setAlertMessage(`${data.message}`);
        } catch (error) {
            setIsDialogOpen(true);
            setAlertMessage(`Error checking connection for ID ${id}: ${error}`);
        }
    };

    useEffect(() => {
        const fetchDatabases = async () => {
            try {
                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_API_BASE_URL}/databases/list${type ? `?type=${type}` : ""}`
                );
                if (!response.ok) {
                    throw new Error("Failed to fetch databases");
                }
                const data = await response.json();
                setDatabases(data.data || []);
            } catch (error) {
                console.error("Error fetching databases:", error);
            } finally {
                setLoading(false);
            }
        };

        if (!isFetched.current) {
            isFetched.current = true;
            fetchDatabases();
        }
    }, [type]);

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
                        <TableHead>Dialect</TableHead>
                        <TableHead>Host</TableHead>
                        <TableHead>Port</TableHead>
                        <TableHead>User</TableHead>
                        <TableHead>Database</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Created At</TableHead>
                        <TableHead>Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {databases.map((db) => (
                        <TableRow key={db.id}>
                            <TableCell className="font-medium">{db.id}</TableCell>
                            <TableCell>{db.name}</TableCell>
                            <TableCell>{db.dialect}</TableCell>
                            <TableCell>{db.host}</TableCell>
                            <TableCell>{db.port}</TableCell>
                            <TableCell>{db.username}</TableCell>
                            <TableCell>{db.database}</TableCell>
                            <TableCell>{db.status === 1 ? "Active" : "Inactive"}</TableCell>
                            <TableCell>{new Date(db.created_at).toLocaleString()}</TableCell>
                            <TableCell>
                                <span
                                    title="Check connection"
                                    onClick={() => checkConnection(db.id)}
                                    className="cursor-pointer"
                                >
                                    <Router/>
                                </span>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>

            <JSAlertDialog
                isOpen={isDialogOpen}
                onClose={() => setIsDialogOpen(false)}
                message={alertMessage}
            />

        </div>
    );
}
