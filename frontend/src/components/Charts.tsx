import { useState, useEffect } from "react";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle
} from "@/components/ui/card";
import { io } from "socket.io-client";

export default function Charts() {
    const [performanceData, setPerformanceData] = useState([
        { name: "Data Ingestion", value: 0 },
        { name: "Data Cleaning", value: 0 },
        { name: "Data Analysis", value: 0 },
        { name: "Insight Generation", value: 0 },
        { name: "Distribution", value: 0 },
    ]);

    const [totalTime, setTotalTime] = useState(0);

    useEffect(() => {
        // Connect to WebSocket
        const socket = io("http://52.38.228.48:5000");

        socket.on("pipeline_update", (data) => {
            if (data.status === "completed" && data.elapsed_time) {
                setPerformanceData(prevData => {
                    const newData = [...prevData];
                    const stepIndex = newData.findIndex(item => item.name === data.step);
                    if (stepIndex !== -1) {
                        newData[stepIndex] = {
                            ...newData[stepIndex],
                            value: data.elapsed_time
                        };
                    }
                    return newData;
                });

                // Update total time
                setTotalTime(prevTotal => prevTotal + data.elapsed_time);
            }
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    const formatMs = (ms: number) => {
        if (ms < 1000) return `${ms}ms`;
        return `${(ms / 1000).toFixed(2)}s`;
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Pipeline Performance</CardTitle>
                <CardDescription>
                    Real-time processing time metrics for each pipeline stage
                </CardDescription>
            </CardHeader>
            <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={performanceData}>
                        <XAxis
                            dataKey="name"
                            tick={{ fontSize: 14 }}
                            textAnchor="end"
                            height={60}
                        />
                        <YAxis
                            tickFormatter={(value) => formatMs(value)}
                        />
                        <Tooltip
                            formatter={(value) => [`${formatMs(Number(value))}`, "Processing Time"]}
                        />
                        <Bar
                            dataKey="value"
                            fill="#2563EB"
                            radius={[4, 4, 0, 0]}
                        />
                    </BarChart>
                </ResponsiveContainer>

                <div className=" grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <p className="text-sm font-medium">Total Stages</p>
                        <p className="text-2xl font-bold">{performanceData.length}</p>
                    </div>
                    <div className="space-y-2">
                        <p className="text-sm font-medium">Total Processing Time</p>
                        <p className="text-2xl font-bold">{formatMs(totalTime)}</p>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}