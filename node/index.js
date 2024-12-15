const express = require('express');
const multer = require('multer');
const { Pool } = require('pg');
const { dbConfig } = require('./config');

const upload = multer({ dest: 'uploads/' });
const pool = new Pool(dbConfig);

const app = express();
app.use(express.json());

app.listen(3000, () => {
    console.log('Server running on port 3000');
});

app.post('/upload', upload.single('file'), async (req, res) => {
    const { originalname, path } = req.file;
    const uploadTime = new Date();
    const status = 'uploaded';

    try {
        const result = await pool.query(
            'INSERT INTO documents (filename, upload_time, status) VALUES ($1, $2, $3) RETURNING id',
            [originalname, uploadTime, status]
        );
        res.json({ documentId: result.rows[0].id });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Failed to upload document' });
    }
});

app.get('/status/:id', async (req, res) => {
    const { id } = req.params;

    try {
        const result = await pool.query(
            'SELECT status FROM documents WHERE id = $1',
            [id]
        );
        if (result.rows.length > 0) {
            res.json({ status: result.rows[0].status });
        } else {
            res.status(404).json({ error: 'Document not found' });
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Failed to fetch status' });
    }
});
