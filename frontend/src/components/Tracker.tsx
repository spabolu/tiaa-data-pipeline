"use client";

import { useState, useEffect } from "react";
import {
  AlertCircle,
  Database,
  FileSpreadsheet,
  LineChart,
  Server,
  CheckCircle2,
  LucideIcon,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { io } from "socket.io-client";
import { Alert, AlertDescription } from "@/components/ui/alert";

interface PipelineStep {
  id: number;
  name: string;
  icon: LucideIcon;
  description: string;
  status: 'pending' | 'in_progress' | 'completed';
  lastUpdate?: string;
}

interface PipelineUpdate {
  step: string;
  status: 'pending' | 'in_progress' | 'completed';
  description?: string;
  timestamp: string;
}

const pipelineSteps: PipelineStep[] = [
  {
    id: 1,
    name: "Data Ingestion",
    icon: Database,
    description: "Collecting raw data from various sources",
    status: "pending",
  },
  {
    id: 2,
    name: "Data Cleaning",
    icon: FileSpreadsheet,
    description: "Preprocessing and cleaning the collected data",
    status: "pending",
  },
  {
    id: 3,
    name: "Data Analysis",
    icon: LineChart,
    description: "Performing statistical analysis",
    status: "pending",
  },
  {
    id: 4,
    name: "Insight Generation",
    icon: AlertCircle,
    description: "Extracting meaningful insights",
    status: "pending",
  },
  {
    id: 5,
    name: "Distribution",
    icon: Server,
    description: "Distributing reports to stakeholders",
    status: "pending",
  },
];

const generateRandomID = () => {
  const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let result = "#";
  for (let i = 0; i < 8; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
};

export default function Tracker() {
  const [steps, setSteps] = useState<PipelineStep[]>(pipelineSteps);
  const [currentStep, setCurrentStep] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string | null>(null);
  const [isCompleted, setIsCompleted] = useState(false);
  const [pipelineID, setPipelineID] = useState("");

  useEffect(() => {
    setPipelineID(generateRandomID());
  }, []);

  useEffect(() => {
    // Check if all steps are completed
    const allCompleted = steps.every(step => step.status === 'completed');
    setIsCompleted(allCompleted);
  }, [steps]);

  useEffect(() => {
    const socket = io("http://52.38.228.48:5000");

    socket.on("connect", () => {
      console.log("Connected to WebSocket server");
      setError(null);
    });

    socket.on("connect_error", (err) => {
      console.error("Connection error:", err);
      setError("Failed to connect to the pipeline server");
    });

    socket.on("pipeline_update", (data: PipelineUpdate) => {
      console.log("Pipeline update received:", data);

      setSteps(prevSteps => {
        const newSteps = [...prevSteps];
        const stepIndex = newSteps.findIndex(step => step.name === data.step);

        if (stepIndex !== -1) {
          // Update the current step
          newSteps[stepIndex] = {
            ...newSteps[stepIndex],
            status: data.status,
            description: data.description || newSteps[stepIndex].description,
            lastUpdate: data.timestamp
          };

          // Mark previous steps as completed
          for (let i = 0; i < stepIndex; i++) {
            newSteps[i] = { ...newSteps[i], status: 'completed' };
          }

          // If this is the last step and it's completed, mark all steps as completed
          if (stepIndex === newSteps.length - 1 && data.status === 'completed') {
            newSteps.forEach(step => step.status = 'completed');
            setCurrentStep(0); // Reset current step to show all completed
          } else {
            setCurrentStep(stepIndex + 1);
          }

          setLastUpdate(data.timestamp);
        }

        return newSteps;
      });
    });

    socket.on("pipeline_error", (data: { error: string }) => {
      console.error("Pipeline error:", data);
      setError(data.error);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="text-center text-3xl text-zinc-900">
            {isCompleted ? (
              <div className="flex items-center justify-center gap-2 text-green-700">
                <CheckCircle2 className="h-8 w-8" />
                <span>Data Pipeline Complete</span>
              </div>
            ) : (
              "Real-Time Data Pipeline Tracker"
            )}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-6">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="relative mb-16">
            {/* Tracker Bar Background */}
            <div className="h-20 rounded-full bg-zinc-200 border-4 border-blue-700">
              {/* Progress Segments */}
              <div className="relative h-full w-full">
                {steps.map((step, index) => {
                  const isCompleted = step.status === 'completed';
                  const isCurrent = step.id === currentStep && !isCompleted;
                  const segmentWidth = `${100 / steps.length}%`;

                  return (
                    <div
                      key={step.id}
                      className={cn(
                        "absolute top-0 h-full transition-all duration-600 ease-in-out",
                        index === 0 && "rounded-l-full",
                        index === steps.length - 1 && "rounded-r-full",
                        isCompleted && "bg-blue-600",
                        isCurrent && "bg-blue-400"
                      )}
                      style={{
                        left: `${(index * 100) / steps.length}%`,
                        width: segmentWidth,
                      }}
                    >
                      {index < steps.length - 1 && (
                        <div
                          className="absolute -right-3 top-0 h-full w-6 overflow-hidden"
                          style={{
                            transform: "skew(-20deg)",
                            zIndex: 1,
                          }}
                        >
                          <div
                            className={cn(
                              "h-full w-full border-2 border-zinc-100",
                              isCompleted ? "bg-blue-200" : "bg-blue-600"
                            )}
                          />
                        </div>
                      )}
                    </div>
                  );
                })}

                {/* Step Icons and Labels */}
                <div className="absolute -bottom-16 flex w-full justify-between px-10">
                  {steps.map((step) => {
                    const isStepCompleted = step.status === 'completed';
                    const isCurrent = step.id === currentStep && !isCompleted;

                    return (
                      <div key={step.id} className="flex flex-col items-center">
                        <div
                          className={cn(
                            "flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all duration-300",
                            isStepCompleted &&
                            "border-blue-900 bg-blue-600 text-white",
                            isCurrent && "border-blue-400 bg-white text-blue-400",
                            !isStepCompleted &&
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
                              isStepCompleted && "text-blue-600",
                              isCurrent && "text-blue-400",
                              !isStepCompleted && !isCurrent && "text-zinc-400"
                            )}
                          >
                            {step.name}
                          </p>
                          <p className="text-xs text-zinc-500">
                            {step.status === 'in_progress' ? 'In Progress' :
                              step.status === 'completed' ? 'Completed' : 'Pending'}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between text-sm text-zinc-500">
          <span>Pipeline ID: {pipelineID}</span>
          {lastUpdate && (
            <span>
              Last Updated:{" "}
              {new Date(lastUpdate).toLocaleTimeString("en-US", {
                timeZone: "America/Phoenix",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
              })}
              {" "}(MST)
            </span>
          )}
        </CardFooter>
      </Card>
    </>
  );
}
