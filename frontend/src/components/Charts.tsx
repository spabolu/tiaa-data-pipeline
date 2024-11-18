import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle
} from "@/components/ui/card";

const performanceData = [
    { name: "Ingestion", value: 4000 },
    { name: "Cleaning", value: 3000 },
    { name: "Analysis", value: 2000 },
    { name: "Insights", value: 2780 },
    { name: "Distribution", value: 2390 },
];


export default function Charts() {
    return (<>
        {/* Charts */}
        <Card>
            <CardHeader>
                <CardTitle>Pipeline Performance</CardTitle>
                <CardDescription>
                    Real-time metrics of your data pipeline
                </CardDescription>
            </CardHeader>
            <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={performanceData}>
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Bar dataKey="value" fill="#dc2626" />{" "}
                    </BarChart>
                </ResponsiveContainer>
                <div className="mt-4 grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <p className="text-sm font-medium">Total Records Processed</p>
                        <p className="text-2xl font-bold">1,234,567</p>
                    </div>
                    <div className="space-y-2">
                        <p className="text-sm font-medium">Average Processing Time</p>
                        <p className="text-2xl font-bold">3.5s</p>
                    </div>
                </div>
            </CardContent>
        </Card>
    </>);
}