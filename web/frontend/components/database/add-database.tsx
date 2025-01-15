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
import JSAlertDialog from "@/components/common/js-alert-dialog";

export default function AddDatabase(
    {
        className,
        ...props
    }: React.ComponentPropsWithoutRef<"div">) {

    // JSAlertDialog
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");

    const [formData, setFormData] = useState({
        host: "",
        password: "",
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

        // Validate required fields
        if (!formData.host || !formData.password) {
            setIsDialogOpen(true);
            setAlertMessage("Host and password are required.");
            return;
        }

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/databases/add`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                setIsDialogOpen(true);
                setAlertMessage("Database added successfully!");
                // setFormData({host: "", password: ""});
            } else {
                const errorData = await response.json();
                setIsDialogOpen(true);
                setAlertMessage(`${errorData.message}`);
            }
        } catch (error) {
            setAlertMessage(`${error}`);
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
                        <div className="grid gap-6">
                            <div className="grid gap-6">
                                <div className="grid gap-2">
                                    <Label htmlFor="host">Host</Label>
                                    <Input
                                        id="host"
                                        type="text"
                                        name="host"
                                        value={formData.host}
                                        onChange={handleInputEvent}
                                        onPaste={handleInputEvent} // Handle paste events
                                        placeholder="localhost"
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
                                <Button type="submit" className="w-full">
                                    Add
                                </Button>
                            </div>
                        </div>
                    </form>
                </CardContent>
            </Card>

            <JSAlertDialog
                isOpen={isDialogOpen}
                onClose={() => setIsDialogOpen(false)}
                message={alertMessage}
            />

        </div>
    );
}
