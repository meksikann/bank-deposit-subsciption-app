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
```

### RUN SENTIMENTOR with Ngrok
1. Open two tunels using ngrok:
```Bash
./ngrok http 7081 -host-header="localhost:7081"
```

```Bash
./ngrok http 8282 -host-header="localhost:8282"
```

2.Copy/paste  URL with 8282 port to
``/home/serg/private/bank-deposit-subsciption-app/src/components/App.jsx.
const backendUrl = <NGROK-URL>
``
3.`
3. RUN CLIENT `npm run start`
4. RUN Recognize server: `~/work/cpd-bot/bot-ui$  ``export GOOGLE_APPLICATION_CREDENTIALS="/home/serg/private/sentiment-8a70878c21a9.json" && npm start`
5. Open browser at <NGROK-URL-WITH-7081-PORT>
