import React from "react";
import "./App.css";

// Import from MUI
import Input from "@mui/joy/Input";
import Grid from "@mui/system/Unstable_Grid";
import Box from "@mui/material/Box";
import LoadingButton from "@mui/lab/LoadingButton";

// Import the API Client
import { Configuration, DefaultApi } from "./api";
import { QueryResponse } from "./api";

const getAPIClient = () => {
  const configuration = new Configuration({
    basePath: "http://localhost:8000",
  });
  const api = new DefaultApi(configuration);
  return api;
};

// Get API Client
const getApiClient = () => {
  return new DefaultApi();
};
function App() {
  // define API client
  const api = getAPIClient();

  // define a state to hold the response from the API
  const [response, setResponse] = React.useState("");
  const [query, setQuery] = React.useState("Nothing Yet");
  const [loading, setLoading] = React.useState(false);

  // define a function to get the text from the query and submit it to the APi
  function getTextFromApi() {
    // set the loading state to true
    setLoading(true);

    // call the API
    let params = {
      prompt: query,
    };
    api.queryQueryPost(params).then((response: QueryResponse) => {
      // set the response to the response from the API
      setResponse(response.response);
      // set the loading state to false
      setLoading(false);
    });
  }

  return (
    <div className="App">
      <Grid container spacing={2}>
        <Grid xs={12} sx={{ m: 4 }}>
          <Box>
            <h1>Chain Texts</h1>
            <p>Enter a prompt and generate a response</p>
            <p>
              Example: "Generate a chain text for me to send around to friends
              about St Patricks Day"
            </p>
          </Box>
        </Grid>

        <Grid xs={12} sx={{ m: 5 }}>
          <Grid xs={8}>
            <Input type="text" onChange={(e) => setQuery(e.target.value)} />
          </Grid>
          <Grid xs={4}>
            <LoadingButton
              onClick={() => getTextFromApi()}
              variant="contained"
              color="primary"
              sx={{ m: 4 }}
              loading={loading}
            >
              Generate Response
            </LoadingButton>
          </Grid>
        </Grid>

        <Grid xs={12}>
          <Box sx={{ m: 4 }}>{response}</Box>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
