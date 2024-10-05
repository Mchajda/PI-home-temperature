import React from "react";
import {
  useQuery,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";
import { Container, Card, CardContent, Typography } from "@mui/material";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface RoomChartProps {
    roomName: string;
  }

// Define the interface for the API response
interface DataProps {
  date: string;
  humidity: number;
  temperature: number;
}

// Function to fetch data from the API
const fetchTemperatureData = async (roomName: string): Promise<DataProps[]> => {
  const response = await fetch(`http://192.168.138.2:5000/data/${roomName}`);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  const apiData = await response.json();
  return apiData.data.map((item: any) => ({
    date: new Date(item.date).toLocaleTimeString(),
    humidity: Number(item.humidity),
    temperature: Number(item.temperature),
  }));
};

export const RoomChart: React.FC<RoomChartProps> = ({roomName}) => {
  const { data, error, isLoading } = useQuery<DataProps[], Error>({
    queryKey: ["temperatureData", roomName] as const,
    queryFn: () => fetchTemperatureData(roomName),
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

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
              <Line
                type="monotone"
                dataKey="temperature"
                stroke="#8884d8"
                activeDot={{ r: 8 }}
              />
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
};
