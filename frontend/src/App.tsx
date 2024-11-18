import { useState } from "react";
import { Waves } from "lucide-react";
import Tracker from "@/components/Tracker";
import Insights from "@/components/Insights";
import Charts from "@/components/Charts";

function App() {
  const [pipelineCompleted, setPipelineCompleted] = useState(false);

  const handleCompletion = (completed: boolean) => {
    setPipelineCompleted(completed);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-zinc-50">
      <div className="flex flex-col w-full max-w-7xl gap-8 p-8">
        <div className="flex items-center justify-center pb-4 border-b border-zinc-300">
          <Waves className="h-8 w-8 text-blue-800 mr-2" />
          <h1 className="text-4xl font-semibold text-blue-800">StreamAI</h1>
        </div>

        <Tracker onCompletion={handleCompletion} />
        <Charts />
        {pipelineCompleted && <Insights />}
      </div>
    </div>
  );
}

export default App;
