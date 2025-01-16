import {useState} from "react";
import {cn} from "@/lib/utils";
import {Button} from "@/components/ui/button";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {Input} from "@/components/ui/input";
import {Label} from "@/components/ui/label";
import {useToast} from "@/hooks/use-toast"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import {Loader} from "lucide-react";

type AddDatabaseProps = React.ComponentPropsWithoutRef<"div"> & {
    type?: string;
};

export default function AddDatabase(
    {
        className,
        type,
        ...props
    }: AddDatabaseProps) {

    const {toast} = useToast()
    const [isLoading, setIsLoading] = useState(false);
    const [formData, setFormData] = useState({
        type: "",
        dialect: "",
        title: "",
        host: "",
        port: "",
        username: "",
        password: "",
        database: "",
    });

    const handleInputEvent = (e: React.ChangeEvent<HTMLInputElement> | React.ClipboardEvent<HTMLInputElement>) => {
        const {name, value} = e.target as HTMLInputElement;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        // Validate required fields
        if (!formData.host || !formData.password) {
            toast({
                variant: "destructive",
                description: "Host and password are required.",
            })
            return;
        }

        formData.type = type ?? '';

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/databases/add`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    toast({
                        description: data.message,
                    })
                    // setFormData({host: "", password: ""});
                } else {
                    toast({
                        variant: "destructive",
                        description: data.message,
                    })
                }
            } else {
                const errorData = await response.json();

                toast({
                    variant: "destructive",
                    description: `${errorData.message}`,
                })
            }
        } catch (error) {
            toast({
                variant: "destructive",
                description: `${error}`,
            })
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className={cn("flex flex-col gap-6", className)} {...props}>
            <Card>
                <CardHeader className="text-center">
                    <CardTitle className="text-xl">Add Database</CardTitle>
                    <CardDescription>Provide your database details</CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit}>

                        <div className="grid grid-cols-1 gap-6 mb-6">
                            <div className="grid gap-2">
                                <Label htmlFor="dialect">Dialect</Label>
                                <Select
                                    onValueChange={(value) =>
                                        setFormData((prev) => ({
                                            ...prev,
                                            dialect: value,
                                        }))
                                    }
                                    name="dialect"
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select a dialect"/>
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectGroup>
                                            <SelectItem value="sqlite">SQLite</SelectItem>
                                            <SelectItem value="mysql">MySQL</SelectItem>
                                            <SelectItem value="postgresql">PostgreSQL</SelectItem>
                                        </SelectGroup>
                                    </SelectContent>
                                </Select>
                                {formData.dialect === "" && (
                                    <span className="text-red-500 text-sm mt-1">Dialect is required.</span>
                                )}
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-6">

                            {/* Left columns */}
                            <div className="grid gap-6">

                                <div className="grid gap-2">
                                    <Label htmlFor="title">Title</Label>
                                    <Input
                                        id="title"
                                        type="text"
                                        name="title"
                                        value={formData.title}
                                        onChange={handleInputEvent}
                                        onPaste={handleInputEvent}
                                        placeholder="MyDB 1"
                                        required
                                    />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="host">Host</Label>
                                    <Input
                                        id="host"
                                        type="text"
                                        name="host"
                                        value={formData.host}
                                        onChange={handleInputEvent}
                                        onPaste={handleInputEvent}
                                        placeholder="localhost"
                                        required
                                    />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="port">Port</Label>
                                    <Input
                                        id="port"
                                        type="number"
                                        name="port"
                                        value={formData.port}
                                        onChange={handleInputEvent}
                                        onPaste={handleInputEvent}
                                        placeholder="3306"
                                        required
                                    />
                                </div>
                            </div>

                            {/* Right columns */}
                            <div className="grid gap-6">
                                <div className="grid gap-2">
                                    <Label htmlFor="username">Username</Label>
                                    <Input
                                        id="username"
                                        type="text"
                                        name="username"
                                        value={formData.username}
                                        onChange={handleInputEvent}
                                        onPaste={handleInputEvent}
                                        placeholder="root"
                                        required
                                    />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="password">Password</Label>
                                    <Input
                                        id="password"
                                        type="password"
                                        name="password"
                                        value={formData.password}
                                        onChange={handleInputEvent}
                                        onPaste={handleInputEvent} // Handle paste events
                                        required
                                    />
                                </div>
                                <div className="grid gap-2">
                                    <Label htmlFor="database">Database Name</Label>
                                    <Input
                                        id="database"
                                        type="text"
                                        name="database"
                                        value={formData.database}
                                        onChange={handleInputEvent}
                                        onPaste={handleInputEvent}
                                        placeholder="Database Name"
                                        required
                                    />
                                </div>
                            </div>
                        </div>
                        <Button type="submit" className="w-full mt-6">
                            {isLoading ? <Loader/> : "Add"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
