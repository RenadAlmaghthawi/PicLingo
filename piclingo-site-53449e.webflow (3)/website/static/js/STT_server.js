const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const speech = require('@google-cloud/speech');

app.use(express.static('public'));
app.use(bodyParser.json());

const client = new speech.SpeechClient();

app.post('/transcribe', async (req, res) => {
    try {
        const audioContent = req.body.audioContent;
        const audio = {
            content: audioContent,
        };

        const config = {
            encoding: 'LINEAR16',
            sampleRateHertz: 16000,
            languageCode: 'en-US',
        };

        const request = {
            audio: audio,
            config: config,
        };

        const [response] = await client.recognize(request);
        const transcription = response.results
            .map(result => result.alternatives[0].transcript)
            .join('\n');
        
        console.log(`Transcription: ${transcription}`);
        res.json({ transcription });
    } catch (error) {
        console.error('Error transcribing speech:', error);
        res.status(500).json({ error: 'An error occurred during transcription' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});