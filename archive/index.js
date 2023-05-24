import express from 'express';
import axios from 'axios';
import AdmZip from 'adm-zip';
import csv from 'csv-writer';
import bibtexParse from 'bibtex-parse-js';

const app = express();
const port = 3000;
app.use(express.json());

app.post('/', async (req, res) => {
  const { email, query, profile } = req.body;

  // Validate the incoming request payload to ensure all required fields are present and properly formatted.
  if (!email || !query || !profile) {
    return res.status(400).json({ error: 'Missing or invalid fields in request payload' });
  }

  // Based on the provided 'profile' field, set the search parameters for spotscience.
  let searchParams = {};
  switch (profile) {
    case 'Daniel Rodrigo Mode':
      searchParams = {
        query,
        years: 60,
        limit: 20,
        doubleBlind: true,
      };
      break;
    case 'Leti Sala Mode':
      searchParams = {
        query,
        years: 10,
        limit: 10,
        metaAnalysis: true,
      };
      break;
    case 'Robles Mode':
      searchParams = {
        query,
        limit: 3,
      };
      break;
    default:
      return res.status(400).json({ error: 'Invalid profile mode' });
  }

  // Initiate a spotscience search with the set parameters on google scholar, pubmed and crossref.
  const searchResults = await axios.post('https://spotscience.herokuapp.com/search', searchParams)
    .then((response) => response.data)
    .catch((error) => {
      console.error(error);
      return res.status(500).json({ error: 'Error in spotscience search' });
    });

  // Download the files from Sci-Hub.
  const zip = new AdmZip();
  const csvWriter = csv.createObjectCsvWriter({
    path: 'articles.csv',
    header: [
      { id: 'title', title: 'Title' },
      { id: 'authors', title: 'Authors' },
      { id: 'journal', title: 'Journal' },
      { id: 'year', title: 'Year' },
      { id: 'doi', title: 'DOI' },
    ],
  });
  const bibtex = [];

  for (const article of searchResults) {
    const { data } = await axios.get(`https://sci-hub.se/${article.doi}`, { responseType: 'arraybuffer' });
    zip.addFile(`${article.title}.pdf`, data);
    csvWriter.writeRecords([{ ...article }]);
    bibtex.push(bibtexParse.toJSON(`@article{${article.title},\n${Object.entries(article).map(([key, value]) => `${key} = {${value}}`).join(',\n')}\n}\n`)[0]);
  }

  zip.addFile('articles.csv', csv.createReadStream());
  zip.addFile('articles.bib', bibtex.map((entry) => entry.entryTags).join('\n\n'));

  // Return a download link for the ZIP folder in the response payload.
  const zipBuffer = zip.toBuffer();
  res.set('Content-Type', 'application/zip');
  res.set('Content-Disposition', `attachment; filename=${query}.zip`);
  res.set('Content-Length', zipBuffer.length);
  res.send(zipBuffer);
});

app.get('/', (req, res) => {
  res.send('Hello, SpotScience!');
});


app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

