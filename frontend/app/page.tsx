"use client";
import React, { useState, ChangeEvent } from "react";

interface SensorData {
  "CO AQI Value": number;
  "Ozone AQI Value": number;
  "NO2 AQI Value": number;
  "PM2.5 AQI Value": number;
}

interface ColorConfig {
  color: string;
  bg: string;
  border: string;
  title: string;
  msg: string;
}

type ColorMapType = Record<string, ColorConfig>;

const App: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorData>({
    "CO AQI Value": 1,
    "Ozone AQI Value": 36,
    "NO2 AQI Value": 0,
    "PM2.5 AQI Value": 51,
  });

  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const defaultMap: ColorConfig = {
    color: "text-gray-700",
    bg: "bg-gray-100",
    border: "border-gray-300",
    title: "Unknown Risk",
    msg: "We received data, but couldn't classify the risk correctly.",
  };

  const colorMap: ColorMapType = {
    Good: {
      color: "text-green-600",
      bg: "bg-green-50",
      border: "border-green-200",
      title: "Excellent Quality",
      msg: "The air is clean. Ideal for outdoor activities!",
    },
    Moderate: {
      color: "text-yellow-600",
      bg: "bg-yellow-50",
      border: "border-yellow-200",
      title: "Moderate Quality",
      msg: "Acceptable, but sensitive individuals should reduce outdoor exertion.",
    },
    "Unhealthy for Sensitive Groups": {
      color: "text-orange-500",
      bg: "bg-orange-50",
      border: "border-orange-200",
      title: "Sensitive Risk",
      msg: "Members of sensitive groups may experience health effects. The general public is likely fine.",
    },
    Unhealthy: {
      color: "text-red-500",
      bg: "bg-red-50",
      border: "border-red-200",
      title: "Unhealthy Air",
      msg: "Avoid prolonged outdoor exertion! Wear a mask.",
    },
    "Very Unhealthy": {
      color: "text-purple-600",
      bg: "bg-purple-50",
      border: "border-purple-200",
      title: "Highly Dangerous",
      msg: "Major health risk. Stay indoors!",
    },
    Hazardous: {
      color: "text-gray-700",
      bg: "bg-gray-100",
      border: "border-gray-300",
      title: "Hazardous",
      msg: "Emergency warning! Toxic conditions.",
    },
  };

  const handleSliderChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSensorData((prev) => ({
      ...prev,
      [name]: parseInt(value, 10),
    }));
  };

  const evaluateAirQuality = async (): Promise<void> => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const url = process.env.NEXT_PUBLIC_URL_API || "http://127.0.0.1:5001";
      const response = await fetch(`${url}/api/v1/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(sensorData),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data.data.prediction_label);
      } else {
        setError(data.message || "Error processing data.");
      }
    } catch (err) {
      setError(
        "Could not connect to the server. Please check if the backend is running.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4 font-sans text-gray-800">
      <div className="bg-white max-w-2xl w-full rounded-2xl shadow-sm border border-gray-100 p-8">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-light text-gray-900 mb-2">AeroActive</h1>
          <p className="text-gray-500 text-sm">
            Real-time air quality monitoring and prediction
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          {Object.entries(sensorData).map(([key, value]) => (
            <div key={key} className="flex flex-col">
              <div className="flex justify-between mb-2">
                <label className="text-sm font-medium text-gray-700">
                  {key.replace(" AQI Value", "")}
                </label>
                <span className="text-sm text-gray-500 font-mono">{value}</span>
              </div>
              <input
                type="range"
                name={key}
                min="0"
                max="200"
                value={value}
                onChange={handleSliderChange}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
            </div>
          ))}
        </div>

        <button
          onClick={evaluateAirQuality}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-4 rounded-xl transition duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {loading ? "Calculating..." : "Evaluate Air Quality"}
        </button>

        <div className="mt-8 min-h-[160px]">
          {error && (
            <div className="p-4 bg-red-50 text-red-600 rounded-xl border border-red-100 text-center text-sm">
              {error}
            </div>
          )}

          {!error && !result && !loading && (
            <div className="p-8 text-center border-2 border-dashed border-gray-200 rounded-xl text-gray-400">
              Adjust the values and click the button to generate a prediction.
            </div>
          )}

          {result && (
            <div
              className={`p-8 rounded-xl border text-center transition-all ${
                (colorMap[result] || defaultMap).bg
              } ${(colorMap[result] || defaultMap).border}`}
            >
              <p className="text-xs uppercase tracking-widest text-gray-500 font-semibold mb-2">
                Identified Risk Index
              </p>
              <h2
                className={`text-3xl font-bold mb-1 ${
                  (colorMap[result] || defaultMap).color
                }`}
              >
                {(colorMap[result] || defaultMap).title}
              </h2>
              <span
                className={`inline-block px-3 py-1 rounded-full text-xs font-bold uppercase mb-4 bg-white shadow-sm ${
                  (colorMap[result] || defaultMap).color
                }`}
              >
                {result}
              </span>
              <p className="text-gray-600 text-sm">
                {(colorMap[result] || defaultMap).msg}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
