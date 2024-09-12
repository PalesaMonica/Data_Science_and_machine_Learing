//server.js
const { spawn } = require('child_process');
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path'); // Import path module to resolve file paths

const app = express();
const port = 3000;

app.use(bodyParser.json());

// Serve static files from the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// Endpoint to get model accuracy
app.get('/model-accuracy', (req, res) => {
    const python = spawn('python', ['train_model.py']);

    python.stdout.on('data', (data) => {
        res.send(data.toString());
    });

    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
});

// Endpoint to make a prediction
app.post('/predict', (req, res) => {
    const inputData = req.body;
    
    // Log input data for debugging
    console.log('Input Data:', inputData);
    
    const python = spawn('python', ['app.py']);
    
    python.stdin.write(JSON.stringify(inputData));
    python.stdin.end();

    python.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`); // Log output from Python script
        res.json(JSON.parse(data));
    });

    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
