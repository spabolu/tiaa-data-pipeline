"use client";

import { useState, useEffect } from "react";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis } from "recharts";
import {
  AlertCircle,
  Database,
  FileSpreadsheet,
  LineChart,
  Server,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";

const pipelineSteps = [
  {
    id: 1,
    name: "Data Ingestion",
    icon: Database,
    description: "Collecting raw data from various sources",
    time: "2 mins ago",
  },
  {
    id: 2,
    name: "Data Cleaning",
    icon: FileSpreadsheet,
    description: "Preprocessing and cleaning the collected data",
    time: "1 min ago",
  },
  {
    id: 3,
    name: "Data Analysis",
    icon: LineChart,
    description: "Performing statistical analysis",
    time: "In progress",
  },
  {
    id: 4,
    name: "Insight Generation",
    icon: AlertCircle,
    description: "Extracting meaningful insights",
    time: "Coming up",
  },
  {
    id: 5,
    name: "Distribution",
    icon: Server,
    description: "Distributing reports to stakeholders",
    time: "Coming up",
  },
];

const performanceData = [
  { name: "Ingestion", value: 4000 },
  { name: "Cleaning", value: 3000 },
  { name: "Analysis", value: 2000 },
  { name: "Insights", value: 2780 },
  { name: "Distribution", value: 2390 },
];

export default function Tracker() {
  const [currentStep, setCurrentStep] = useState(1);
  const [isAutoAdvancing, setIsAutoAdvancing] = useState(false);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isAutoAdvancing) {
      interval = setInterval(() => {
        setCurrentStep((prevStep) => {
          if (prevStep < pipelineSteps.length) {
            return prevStep + 1;
          } else {
            setIsAutoAdvancing(false);
            return prevStep;
          }
        });
      }, 2000); // Advance every 2 seconds
    }
    return () => clearInterval(interval);
  }, [isAutoAdvancing]);

  const handleAdvance = () => {
    if (currentStep < pipelineSteps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleAutoAdvance = () => {
    setIsAutoAdvancing(!isAutoAdvancing);
    if (currentStep === pipelineSteps.length) {
      setCurrentStep(1);
    }
  };

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="text-center text-3xl">
            Data Pipeline Tracker
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="relative mb-16">
            {/* Tracker Bar Background */}
            <div className="h-20 rounded-full bg-zinc-200 border-4 border-red-600">
              {/* Progress Segments */}
              <div className="relative h-full w-full">
                {pipelineSteps.map((step, index) => {
                  const isCompleted = step.id < currentStep;
                  const isCurrent = step.id === currentStep;
                  const segmentWidth = `${100 / pipelineSteps.length}%`;

                  return (
                    <div
                      key={step.id}
                      className={cn(
                        "absolute top-0 h-full transition-all duration-600 ease-in-out",
                        index === 0 && "rounded-l-full",
                        index === pipelineSteps.length - 1 && "rounded-r-full",
                        isCompleted && "bg-red-600",
                        isCurrent && "bg-red-400"
                      )}
                      style={{
                        left: `${(index * 100) / pipelineSteps.length}%`,
                        width: segmentWidth,
                      }}
                    >
                      {index < pipelineSteps.length - 1 && (
                        <div
                          className="absolute -right-3 top-0 h-full w-6 overflow-hidden"
                          style={{
                            transform: "skew(-20deg)",
                            zIndex: 1,
                          }}
                        >
                          <div
                            className={cn(
                              "h-full w-full",
                              isCompleted ? "bg-red-200" : "bg-red-600"
                            )}
                          />
                        </div>
                      )}
                    </div>
                  );
                })}

                {/* Step Icons and Labels */}
                <div className="absolute -bottom-16 flex w-full justify-between px-10">
                  {pipelineSteps.map((step) => {
                    const isCompleted = step.id < currentStep;
                    const isCurrent = step.id === currentStep;

                    return (
                      <div key={step.id} className="flex flex-col items-center">
                        <div
                          className={cn(
                            "flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all duration-300",
                            isCompleted &&
                              "border-red-900 bg-red-600 text-white",
                            isCurrent && "border-red-400 bg-white text-red-400",
                            !isCompleted &&
                              !isCurrent &&
                              "border-zinc-300 bg-white text-zinc-300"
                          )}
                        >
                          <step.icon className="h-5 w-5" />
                        </div>
                        <div className="mt-2 text-center">
                          <p
                            className={cn(
                              "text-sm font-semibold",
                              isCompleted && "text-red-600",
                              isCurrent && "text-red-400",
                              !isCompleted && !isCurrent && "text-zinc-400"
                            )}
                          >
                            {step.name}
                          </p>
                          <p className="text-xs text-zinc-500">{step.time}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
          <div className="pt-8">
            <div className="flex justify-center space-x-4">
              <Button
                onClick={handleAdvance}
                disabled={
                  currentStep === pipelineSteps.length || isAutoAdvancing
                }
              >
                Advance Step
              </Button>
              <Button onClick={handleAutoAdvance} variant="outline">
                {isAutoAdvancing ? "Stop Auto Advance" : "Start Auto Advance"}
              </Button>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between text-sm text-zinc-500">
          <span>Pipeline ID: #A1B2C3D4</span>
          {/* <span>
            Est. Completion: {pipelineSteps.length - currentStep + 1} minutes
          </span> */}
        </CardFooter>
      </Card>

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
    </>
  );
}
