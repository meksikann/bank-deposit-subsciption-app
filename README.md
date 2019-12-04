## dataset origin:
 `https://archive.ics.uci.edu/ml/datasets/Bank+Marketing`
 
## Dependencies

To install the boilerplate dependencies, you can run:

```bash
npm install --no-optional
pip install -r requirements.txt
```

## Quickstart

Once the dependencies are installed, you can start the api with the following command:

```bash
npm run production
```

That will start the server on port 7082. To run the development server with hot module reloading, run:

```bash
npm run start
```

That will start the webpack dev server on port 7081.

## Tests

To run the Javascript tests (located in `src/tests/`), run:

```bash
npm run jest
```

To run the Python tests (located in `server/tests/`), run:

```bash
pytest
