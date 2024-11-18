import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function Insights() {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  useEffect(() => {
    const fetchPdf = async () => {
      try {
        const response = await fetch('http://52.38.228.48:5000/download_report', {
          method: 'GET',
        });

        if (!response.ok) {
          throw new Error('Failed to fetch the PDF');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setPdfUrl(url);
      } catch (error) {
        console.error('Error fetching the PDF:', error);
      }
    };

    fetchPdf();
  }, []);

  return (
    <div>
      <Card>
        <CardHeader>
          <CardTitle className="text-center text-3xl text-zinc-900">Business Insights</CardTitle>
        </CardHeader>
        <CardContent>
          {pdfUrl ? (
            <iframe
              src={pdfUrl}
              width="100%"
              height="800px"
              title="Business Report"
            ></iframe>
          ) : (
            <p>Loading PDF...</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
