import Tracker from "@/components/Tracker";
import FileUpload from "@/components/FileUpload";
import { Waves } from "lucide-react";
import Charts from "@/components/Charts";

function App() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-zinc-50">
      <div className="flex flex-col w-full max-w-7xl gap-8 p-8">
        <div className="flex items-center justify-center pb-4 border-b border-zinc-300">
          <Waves className="h-8 w-8 text-zinc-800 mr-2" />
          <h1 className="text-4xl font-semibold text-zinc-800">StreamAI</h1>
        </div>

        <FileUpload />
        <Tracker />
        <Charts />
      </div>
    </div>
  );
}

export default App;
