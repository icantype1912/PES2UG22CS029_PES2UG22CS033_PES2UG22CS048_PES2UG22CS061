import './App.css';
import { TextField, Button, Card, CardContent, Typography } from '@mui/material';
import { useState } from 'react';

function App() {
  const [originalUrl, setOriginalUrl] = useState('');
  const [shortenedUrl, setShortenedUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [expandedUrl, setExpandedUrl] = useState('');

  const handleShorten = async () => {
    try {
      const response = await fetch('/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: originalUrl })
      });
      const data = await response.json();
      setShortenedUrl(data.short_url);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleExpand = async () => {
    try {
      const response = await fetch(`/expand/${shortUrl}`);
      const data = await response.json();
      setExpandedUrl(data.original_url);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <div className="header">
        <h1 className="header-title">URL-Shortener with Load Balancing</h1>
      </div>
      <div className="wrap">
        <div className="main-web">
          <div className="main-web-left">
            <Card sx={{ padding: 2, margin: 2 }}>
              <CardContent>
                <Typography variant="h6">Shorten a URL</Typography>
                <TextField
                  label="Enter Long URL"
                  fullWidth
                  variant="outlined"
                  value={originalUrl}
                  onChange={(e) => setOriginalUrl(e.target.value)}
                  sx={{ my: 2 }}
                />
                <Button variant="contained" onClick={handleShorten}>Shorten</Button>
                {shortenedUrl && (
                  <Typography sx={{ mt: 2 }}>Short URL: <a href={shortenedUrl}>{shortenedUrl}</a></Typography>
                )}
              </CardContent>
            </Card>
          </div>
          <div className="main-web-right">
            <Card sx={{ padding: 2, margin: 2 }}>
              <CardContent>
                <Typography variant="h6">Get Original URL</Typography>
                <TextField
                  label="Enter Short URL Code"
                  fullWidth
                  variant="outlined"
                  value={shortUrl}
                  onChange={(e) => setShortUrl(e.target.value)}
                  sx={{ my: 2 }}
                />
                <Button variant="contained" onClick={handleExpand}>Get Original</Button>
                {expandedUrl && (
                  <Typography sx={{ mt: 2 }}>Original URL: <a href={expandedUrl}>{expandedUrl}</a></Typography>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
        <div className="test">
          <div className="test-left"></div>
          <div className="test-right"></div>
        </div>
      </div>
    </div>
  );
}

export default App;
