import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function Insights() {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  useEffect(() => {
    const fetchPdf = async () => {
      try {
        const response = await fetch('http://52.38.228.48:5000/download_pdf', {
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
  
            <Button
              onClick={async () => {
                const response = await fetch('http://52.38.228.48:5000/download_transcript');
                if (response.ok) {
                  const blob = await response.blob();
                  const url = URL.createObjectURL(blob);
                  window.open(url, '_blank'); // Open the HTML file in a new tab
                } else {
                  console.error('Failed to fetch transcript.html');
                }
              }}
              className="text-center text-zinc-800 mt-4"
            >
              Open transcript.html
            </Button>
            <Button
              onClick={async () => {
                const response = await fetch('http://52.38.228.48:5000/download_profile');
                if (response.ok) {
                  const blob = await response.blob();
                  const url = URL.createObjectURL(blob);
                  window.open(url, '_blank'); // Open the HTML file in a new tab
                } else {
                  console.error('Failed to fetch profile.html');
                }
              }}
              className="text-center text-zinc-800 mt-4"
            >
              Open profile.html
            </Button>
            <Button
              onClick={async () => {
                const response = await fetch('http://52.38.228.48:5000/download_portfolio');
                if (response.ok) {
                  const blob = await response.blob();
                  const url = URL.createObjectURL(blob);
                  window.open(url, '_blank'); // Open the HTML file in a new tab
                } else {
                  console.error('Failed to fetch portfolio.html');
                }
              }}
              className="text-center text-zinc-800 mt-4"
            >
              Open portfolio.html
            </Button>
        </CardContent>
      </Card>
    </div>
  );
}
