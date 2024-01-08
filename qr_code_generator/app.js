const express = require('express');
const qr = require('qr-image');
const path = require('path'); // Import the 'path' module

const app = express();
const port = 3000;

app.use(express.json());

// Endpoint to generate QR code
app.get('/str2qr', (req, res) => {
    const { text } = req.query;

    if (!text) {
        return res.status(400).json({ error: 'Missing "text" parameter.' });
    }

    const qrImage = qr.image(text, { type: 'png' });
    res.type('png');
    qrImage.pipe(res);
});

// Serve the HTML file at the root endpoint
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
