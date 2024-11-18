import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

// Define the interface for the output data
interface LLMOutputData {
  step: string;
  status: string;
  description?: string;
  elapsed_time?: number;
  timestamp: string;
}

const socket = io('http://52.38.228.48:5000/');

export default function LLMOutput() {
  // Initialize the state with the correct type
  const [outputs, setOutputs] = useState<LLMOutputData[]>([]);

  useEffect(() => {
    // Listen for 'pipeline_update' events
    socket.on('pipeline_update', (data: LLMOutputData) => {
      setOutputs((prevOutputs) => [...prevOutputs, data]);
    });

    // Listen for 'pipeline_error' events
    socket.on('pipeline_error', (error: { error: string }) => {
      setOutputs((prevOutputs) => [
        ...prevOutputs,
        { step: 'Error', status: 'failed', description: error.error, timestamp: new Date().toISOString() },
      ]);
    });

    // Cleanup on unmount
    return () => {
      socket.off('pipeline_update');
      socket.off('pipeline_error');
    };
  }, []);

  return (
    <div style={{ padding: '1rem', fontFamily: 'Arial, sans-serif' }}>
      <h2>Live LLM Output</h2>
      <ul>
        {outputs.map((output, index) => (
          <li key={index} style={{ marginBottom: '1rem' }}>
            <strong>Step:</strong> {output.step} <br />
            <strong>Status:</strong> {output.status} <br />
            {output.description && (
              <>
                <strong>Description:</strong> {output.description} <br />
              </>
            )}
            {output.elapsed_time !== undefined && (
              <>
                <strong>Elapsed Time:</strong> {output.elapsed_time} ms <br />
              </>
            )}
            <strong>Timestamp:</strong> {output.timestamp}
          </li>
        ))}
      </ul>
    </div>
  );
}
