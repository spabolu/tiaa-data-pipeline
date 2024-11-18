import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Terminal, FileCode, Database } from "lucide-react";

interface CodeSnippet {
  stage: string;
  code: string;
  timestamp: string;
  type: 'sql' | 'python' | 'output';
}

export default function LLMOutput() {
  const [codeSnippets, setCodeSnippets] = useState<CodeSnippet[]>([]);
  const [activeTab, setActiveTab] = useState("all");
  
  useEffect(() => {
    const socket = io("http://52.38.228.48:5000");

    socket.on("pipeline_code", (data: CodeSnippet) => {
      setCodeSnippets(prev => [...prev, data]);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const filteredSnippets = activeTab === "all" 
    ? codeSnippets 
    : codeSnippets.filter(snippet => snippet.type === activeTab);

  return (
    <Card className="mt-4">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Terminal className="h-5 w-5" />
            <CardTitle>Live Pipeline Code</CardTitle>
          </div>
        </div>
        <CardDescription>
          Real-time code execution and output from the pipeline
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="all" value={activeTab} onValueChange={setActiveTab}>
          <TabsList>
            <TabsTrigger value="all" className="flex items-center gap-2">
              <FileCode className="h-4 w-4" />
              All
            </TabsTrigger>
            <TabsTrigger value="python" className="flex items-center gap-2">
              <Terminal className="h-4 w-4" />
              Python
            </TabsTrigger>
            <TabsTrigger value="sql" className="flex items-center gap-2">
              <Database className="h-4 w-4" />
              SQL
            </TabsTrigger>
            <TabsTrigger value="output" className="flex items-center gap-2">
              <Terminal className="h-4 w-4" />
              Output
            </TabsTrigger>
          </TabsList>
          <ScrollArea className="h-[400px] mt-4 rounded-md border p-4">
            <div className="space-y-4">
              {filteredSnippets.map((snippet, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex items-center justify-between text-sm text-zinc-500">
                    <span className="font-semibold text-zinc-700">
                      {snippet.stage}
                    </span>
                    <span>{formatTimestamp(snippet.timestamp)}</span>
                  </div>
                  <pre className="overflow-x-auto rounded-lg bg-zinc-950 p-4">
                    <code className="text-sm text-zinc-50">{snippet.code}</code>
                  </pre>
                </div>
              ))}
              {filteredSnippets.length === 0 && (
                <div className="flex h-[300px] items-center justify-center text-zinc-500">
                  <p>No code output yet...</p>
                </div>
              )}
            </div>
          </ScrollArea>
        </Tabs>
      </CardContent>
    </Card>
  );
}