import { Upload, X, FileText, Folder } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useState, useCallback } from "react";

// File type interface
interface FileType {
  name: string;
  size: number;
  type: string;
  lastModified: number;
  content?: File;
}

export default function FileUpload(): JSX.Element {
  const [files, setFiles] = useState<FileType[]>([]);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleDragOver = useCallback(
    (e: React.DragEvent<HTMLDivElement>): void => {
      e.preventDefault();
      setIsDragging(true);
    },
    []
  );

  const handleDragLeave = useCallback(
    (e: React.DragEvent<HTMLDivElement>): void => {
      e.preventDefault();
      setIsDragging(false);
    },
    []
  );

  const handleDrop = useCallback(
    async (e: React.DragEvent<HTMLDivElement>): Promise<void> => {
      e.preventDefault();
      setIsDragging(false);
      setError("");

      const items = Array.from(e.dataTransfer.items);
      const newFiles: FileType[] = items
        .map((item) => {
          const dataTransferItem = item as DataTransferItem;
          if (dataTransferItem.kind === "file") {
            const file = dataTransferItem.getAsFile();
            if (file) {
              return {
                name: file.name,
                size: file.size,
                type: file.type,
                lastModified: file.lastModified,
                content: file, // Add the file object for uploading
              };
            }
          }
          return null;
        })
        .filter(Boolean) as FileType[];

      // Update the files state
      setFiles((prev) => [...prev, ...newFiles]);

      // Process only .zip files for backend upload
      for (const file of newFiles) {
        if (file.name.endsWith(".zip")) {
          try {
            const formData = new FormData();
            formData.append("file", file.content as File);

            console.log(`Uploading ${file.name} to the backend...`);
            // Send POST request to upload .zip file
            const response = await fetch('http://127.0.0.1:5000/upload', {
              method: "POST",
              body: formData,
            });

            if (!response.ok) {
              setError(`Failed to upload ${file.name} to the backend.`);
            } else {
              console.log(`${file.name} uploaded successfully!`);
            }
          } catch (err) {
            setError(`Error uploading ${file.name}: ${(err as Error).message}`);
          }
        }
      }
    },
    []
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>): void => {
      const selectedFiles = Array.from(e.target.files || []);
      const newFiles: FileType[] = selectedFiles.map((file) => ({
        name: file.name,
        size: file.size,
        type: file.type,
        lastModified: file.lastModified,
      }));
      setFiles((prev) => [...prev, ...newFiles]);
    },
    []
  );

  const removeFile = useCallback((index: number): void => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-5 w-5" />
            Upload Data Files
          </CardTitle>
          <CardDescription>
            Start by uploading the files you want to process
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`relative mb-4 flex min-h-40 flex-col items-center justify-center rounded-lg border-2 border-dashed p-6 transition-colors ${
              isDragging
                ? "border-red-500 bg-red-50"
                : "border-zinc-300 hover:border-red-500"
            }`}
          >
            <input
              type="file"
              multiple
              onChange={handleFileInput}
              className="absolute inset-0 cursor-pointer opacity-0"
            />
            <Upload
              className={`mb-4 h-12 w-12 ${
                isDragging ? "text-red-500" : "text-zinc-400"
              }`}
            />
            <p className="mb-2 text-sm font-medium">
              Drag and drop files here or click to browse
            </p>
            <p className="text-xs text-zinc-500">
              Support for single or bulk upload
            </p>
          </div>

          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            {files.map((file, index) => (
              <div
                key={`${file.name}-${index}`}
                className="flex items-center justify-between rounded-lg border p-3 shadow-sm"
              >
                <div className="flex items-center space-x-3">
                  {file.type.includes("folder") ? (
                    <Folder className="h-5 w-5 text-blue-500" />
                  ) : (
                    <FileText className="h-5 w-5 text-zinc-500" />
                  )}
                  <div>
                    <p className="text-sm font-medium">{file.name}</p>
                    <p className="text-xs text-zinc-500">
                      {formatFileSize(file.size)}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="rounded-full p-1 hover:bg-zinc-100"
                >
                  <X className="h-4 w-4 text-zinc-500" />
                </button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </>
  );
}
