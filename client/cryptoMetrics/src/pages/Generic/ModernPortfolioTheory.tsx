import { IonCard, IonCardContent, IonContent } from "@ionic/react";
import axios from "axios";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import highContrastDark from "highcharts/themes/high-contrast-dark";
import { useEffect, useState } from "react";

highContrastDark(Highcharts);

const ModernPortfolioAnalysis: React.FC = () => {
  const [portfolioSimulations, setPortfolioSimulations] = useState<any[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [maxSharpeRatio, setMaxSharpeRatio] = useState<{
    BTC_weight: number;
    ETH_weight: number;
    expected_return: number;
    sharpe_ratio: number;
    volatility: number;
  }>({
    volatility: 0,
    expected_return: 0,
    BTC_weight: 0,
    ETH_weight: 0,
    sharpe_ratio: 0
  });

  useEffect(() => {
    axios.get("http://localhost:5000/api/analysis/modern-portfolio-analysis")
      .then(response => {
        setPortfolioSimulations(response.data.portfolio_simulations);
        setMaxSharpeRatio(response.data.max_sharpe_ratio);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  useEffect(() => {
    const convertedData = portfolioSimulations.map(portfolio => ({
      x: portfolio.volatility,
      y: portfolio.expected_return * 100,
      BTC_weight: (portfolio.BTC_weight * 100).toFixed(2),
      ETH_weight: (portfolio.ETH_weight * 100).toFixed(2),
    }));

    setChartData(convertedData);
  }, [portfolioSimulations]);

  const options: Highcharts.Options = {
    chart: {
      height: 800,
      reflow: true
    },
    title: {
      text: '',
    },
    xAxis: {
      title: {
        text: 'Volatility',
      },
    },
    yAxis: {
      title: {
        text: 'Expected Return (%) in the next 365 days',
      },
      gridLineColor: 'rgba(128, 128, 128, 0.05)'
    },
    series: [
      {
        name: 'Portfolio Simulations',
        type: 'scatter',
        data: chartData,
        tooltip: {
          headerFormat: '<b>Portfolio Simulation</b><br>',
          pointFormat: '<br>BTC Weight: {point.BTC_weight}%<br>ETH Weight: {point.ETH_weight}%<br>Expected Return: {point.y:.2f}%<br>Volatility: {point.x:.4f}'
        }
      },
      {
        name: 'Max Sharpe Ratio',
        type: 'scatter',
        data: [{ x: maxSharpeRatio.volatility, y: maxSharpeRatio.expected_return * 100, BTC_weight: (maxSharpeRatio.BTC_weight * 100).toFixed(2), ETH_weight: (maxSharpeRatio.ETH_weight * 100).toFixed(2) }],
        marker: {
          symbol: 'circle',
          radius: 10,
          fillColor: '#B84000',
          lineWidth: 0
        },
        tooltip: {
          headerFormat: '<b>Max Sharpe Ratio</b><br>',
          pointFormat: '<br>BTC Weight: {point.BTC_weight}%<br>ETH Weight: {point.ETH_weight}%<br>Expected Return: {point.y:.2f}%<br>Volatility: {point.x:.4f}'
        }
      }
    ],
    credits: {
      enabled: false,
    }
  };

  return (
    <IonContent>
      <IonCard>
        <HighchartsReact highcharts={Highcharts} options={options} />
      </IonCard>

      <IonCard>
        <IonCardContent className="description-card">
          <h2>Description</h2>
          <div>
              Modern Portfolio Analysis is a quantitative method used in finance to assess and optimize investment portfolios. It involves the evaluation of various assets, including cryptocurrencies like Bitcoin and Ethereum, to determine the most efficient allocation that balances risk and return.
          </div>
          <div>
              The primary objective of Modern Portfolio Analysis is to create a diversified portfolio that maximizes potential returns for a given level of risk or minimizes risk for a desired level of return. This analysis takes into account the correlations between different assets and seeks to find the optimal allocation that achieves the best risk-return trade-off.
          </div>
          <div>
              Modern Portfolio Analysis is based on the principles of the Efficient Frontier and Capital Asset Pricing Model (CAPM), aiming to achieve the highest level of return for a given level of risk exposure in the context of various assets, including cryptocurrencies like Bitcoin and Ethereum.
          </div>
          <div>
              By considering the historical performance and interactions among different assets, this approach aids investors in making informed decisions, constructing well-balanced portfolios, and achieving their financial goals across a diverse range of investment options.
          </div>
        </IonCardContent>
      </IonCard>

    </IonContent>
  );
};
  
export default ModernPortfolioAnalysis;
