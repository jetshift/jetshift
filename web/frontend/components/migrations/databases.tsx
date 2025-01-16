import {useEffect, useState, useRef} from "react";
import {cn} from "@/lib/utils";
import {Loader, CircleX} from "lucide-react";
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

interface MigrateDatabase {
    id: number;
    title: string;
    source_db: string;
    target_db: string;
    status: boolean;
    logs: string;
    created_at: string;
    updated_at: string;
}

type ListDatabaseProps = React.ComponentPropsWithoutRef<"div">

export default function ListMigrationDatabase(
    {
        className,
        ...props
    }: ListDatabaseProps) {

    const {toast} = useToast()
    const [databases, setDatabases] = useState<MigrateDatabase[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const isFetchedDatabases = useRef(false);
    const [isDeletingDatabase, setDeletingDatabase] = useState<number | null>(null);

    const fetchDatabases = async () => {
        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_BASE_URL}/migrations/databases`
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
                fetchDatabases();
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
            fetchDatabases();
        }
    });

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
                        <TableHead>Source DB</TableHead>
                        <TableHead>Target DB</TableHead>
                        <TableHead>Logs</TableHead>
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
                            <TableCell>{db.source_db}</TableCell>
                            <TableCell>{db.target_db}</TableCell>
                            <TableCell>{db.logs}</TableCell>
                            <TableCell>{db.status ? "Active" : "Inactive"}</TableCell>
                            <TableCell>{new Date(db.created_at).toLocaleString()}</TableCell>
                            <TableCell className="flex items-center space-x-2">
                                <span
                                    title={"Delete job"}
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
