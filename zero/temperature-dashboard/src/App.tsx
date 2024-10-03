import React, { useEffect, useState } from "react";
import { Container, Card, CardContent, Typography } from "@mui/material";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import "./App.css";

interface ApiResponse {
  date: string;
  humidity: string;
  temperature: string;
}

interface DataProps {
  date: string;
  humidity: number;
  temperature: number;
}

function App() {
  const [data, setData] = useState<DataProps[]>([]);

  useEffect(() => {
    // Fetch data from API
    fetch("http://192.168.138.2:5000/data/outside")
      .then((response) => response.json())
      .then((apiData) => {
        // Convert API response to the format required for the chart
        const formattedData = apiData.data.map((item: ApiResponse) => ({
          date: new Date(item.date).toLocaleTimeString(), // Convert date to readable time
          humidity: Number(item.humidity), // Convert humidity to number
          temperature: Number(item.temperature), // Convert temperature to number
        }));
        setData(formattedData); // Update the state with formatted data
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <Container>
      <Card sx={{ height: 600 }}>
        <CardContent sx={{ height: 400 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              width={500}
              height={300}
              data={data}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="temperature" stroke="#8884d8" activeDot={{ r: 8 }} />
              <Line type="monotone" dataKey="humidity" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
          <Typography gutterBottom variant="h5" component="div">
            Temperature and Humidity Data
          </Typography>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            This chart displays the temperature and humidity data over time.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
}

export default App;
