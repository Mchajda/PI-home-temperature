import { RoomChart } from "./components/RoomChart";
import { Container, Card, CardContent, Typography } from "@mui/material";
import Grid from "@mui/material/Grid2";
import "./App.css";

function App() {
  return (
    // <Container sx={{ '> *': {my: 2} }}>
    //   <RoomChart roomName={"outside"} />
    //   <RoomChart roomName={"bedroom"} />
    //   <RoomChart roomName={"living_room"} />
    //   <RoomChart roomName={"office"} />
    // </Container>

    <Container>
      <Grid container spacing={2}>
        <Grid size={6}>
          <RoomChart roomName={"outside"} />
        </Grid>
        <Grid size={6}>
          <RoomChart roomName={"bedroom"} />
        </Grid>
        <Grid size={6}>
          <RoomChart roomName={"living_room"} />
        </Grid>
        <Grid size={6}>
          <RoomChart roomName={"office"} />
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;
