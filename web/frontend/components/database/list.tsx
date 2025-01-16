import {useEffect, useState, useRef} from "react";
import {cn} from "@/lib/utils";
import {Router, Loader, CircleX} from "lucide-react";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {useToast} from "@/hooks/use-toast"

interface Database {
    id: number;
    type: string;
    title: string;
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

    const {toast} = useToast()
    const [databases, setDatabases] = useState<Database[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const isFetchedDatabases = useRef(false);
    const [isCheckingConnection, setCheckingConnection] = useState<number | null>(null);
    const [isDeletingDatabase, setDeletingDatabase] = useState<number | null>(null);

    const fetchDatabases = async (type?: string) => {
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
            toast({
                variant: "destructive",
                description: `Error fetching databases: ${error}`,
            })
        } finally {
            setLoading(false);
        }
    };

    const checkConnection = async (id: number) => {
        try {
            setCheckingConnection(id);

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

            if (data.success) {
                toast({
                    description: `${data.message}`,
                })
            } else {
                toast({
                    variant: "destructive",
                    description: `${data.message}`,
                })
            }
        } catch (error) {
            toast({
                variant: "destructive",
                description: `Error checking connection for ID ${id}: ${error}`,
            })
        } finally {
            setCheckingConnection(null);
        }
    };

    const deleteDatabase = async (id: number) => {
        try {
            setDeletingDatabase(id);

            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_BASE_URL}/databases/delete/${id}`,
                {
                    method: "POST",
                }
            );
            if (!response.ok) {
                throw new Error("Failed to delete database");
            }
            const data = await response.json();

            if (data.success) {
                fetchDatabases(type);
                toast({
                    description: `${data.message}`,
                })
            } else {
                toast({
                    variant: "destructive",
                    description: `${data.message}`,
                })
            }
        } catch (error) {
            toast({
                variant: "destructive",
                description: `Error checking connection for ID ${id}: ${error}`,
            })
        } finally {
            setDeletingDatabase(null);
        }
    };

    useEffect(() => {
        if (!isFetchedDatabases.current) {
            isFetchedDatabases.current = true;
            fetchDatabases(type);
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
                        <TableHead>Title</TableHead>
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
                            <TableCell>{db.title}</TableCell>
                            <TableCell>{db.dialect}</TableCell>
                            <TableCell>{db.host}</TableCell>
                            <TableCell>{db.port}</TableCell>
                            <TableCell>{db.username}</TableCell>
                            <TableCell>{db.database}</TableCell>
                            <TableCell>{db.status ? "Active" : "Inactive"}</TableCell>
                            <TableCell>{new Date(db.created_at).toLocaleString()}</TableCell>
                            <TableCell className="flex items-center space-x-2">
                               <span
                                   title={isCheckingConnection === db.id ? "Checking connection..." : "Check connection"}
                                   onClick={() => checkConnection(db.id)}
                                   className={`cursor-pointer ${
                                       isCheckingConnection === db.id ? "opacity-50 pointer-events-none" : ""
                                   }`}
                               >
                                {isCheckingConnection === db.id ? <Loader/> : <Router color={"#4663AC"}/>}
                                </span>
                                <span
                                    title={"Delete database"}
                                    onClick={() => deleteDatabase(db.id)}
                                >
                                {isDeletingDatabase === db.id ? <Loader/> : <CircleX color={"#E3646F"}/>}
                                </span>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
}
