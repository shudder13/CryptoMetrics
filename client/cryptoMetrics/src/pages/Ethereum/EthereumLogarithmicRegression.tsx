import { IonCard, IonCardContent, IonContent } from "@ionic/react";
import axios from "axios";
import Highcharts from 'highcharts';
import HighchartsReact from "highcharts-react-official";
import highContrastDark from 'highcharts/themes/high-contrast-dark';
import { useEffect, useState } from "react";
import '../Page.css';

highContrastDark(Highcharts);

const EthereumLogarithmicRegression: React.FC = () => {
  const [priceData, setPriceData] = useState<any[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [regressionData, setRegressionData] = useState<any[]>([]);
  const [showBitcoinHalvingDates, setShowBitcoinHalvingDates] = useState<boolean>(false);
  const BitcoinHalvingDates = ['2012-11-28', '2016-07-09', '2020-05-11', '2024-04-01', '2028-01-01'];
  const BitcoinHalvingDatesColor = '#FFFFFF';

  useEffect(() => {
    axios.get("http://localhost:5000/api/price-history/crypto/ETH")
      .then(response => {
        setPriceData(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  useEffect(() => {
    const convertedData = Object.entries(priceData).map(([date, value]) => {
      return [new Date(date).getTime(), value.close];
    });

    setChartData(convertedData);
  }, [priceData]);

  useEffect(() => {
    axios.get("http://localhost:5000/api/analysis/logarithmic-regression/ETH")
      .then(response => {
        const regressionDict = response.data;
        const regressionArray = [];
  
        for (const date in regressionDict) {
          const timestamp = new Date(date).getTime();
          const price = regressionDict[date];
          regressionArray.push([timestamp, price]);
        }
  
        setRegressionData(regressionArray);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  const options: Highcharts.Options = {
    chart: {
      height: 800,
      reflow: true,
      zooming: {
        type: 'x'
      }
    },
    title: {
      text: '',
    },
    xAxis: {
      type: 'datetime',
      dateTimeLabelFormats: {
        day: '%e of %b, %Y'
      },
      plotLines: showBitcoinHalvingDates 
        ? BitcoinHalvingDates.map(date => ({
          value: new Date(date).getTime(),
          color: BitcoinHalvingDatesColor,
          width: 0.4,
        })) : [],
    },
    yAxis: {
      title: {
        text: 'Price ($)'
      },
      type: 'logarithmic',
      gridLineColor: 'rgba(128, 128, 128, 0.05)'
    },
    series: [
      {
        type: 'line',
        data: chartData,
        name: 'Ethereum price',
      },
      {
        type: 'line',
        data: regressionData,
        name: 'Regression',
        color: '#FFA500',
      },
      {
        type: 'line',
        data: [],
        name: 'Bitcoin Halvings',
        color: BitcoinHalvingDatesColor,
        visible: showBitcoinHalvingDates
      }
    ],
    plotOptions: {
        series: {
          events: {
            legendItemClick: function(event) {
              if (this.name === 'Bitcoin Halvings') {
                setShowBitcoinHalvingDates(!showBitcoinHalvingDates);
              }
            }
          }
        }
      },
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
            Regressions are a set of statistical techniques used to model and analyze the relationship between one or more independent variables (time in this case) and dependent variables (Ethereum's price in this case).
          </div>
          <div>
            The primary purpose of regression analysis is to predict or estimate the value of the dependent variable based on the values of the independent variables.
          </div>
          <div>
            Logarithmic regression is a specific type of nonlinear regression used when the relationship between the variables is best represented by a logarithmic function. This type of regression is often employed when the data exhibits logarithmic growth or decay, and a straight line would not fit the data adequately.
          </div>
          <div>
            Regression analysis helps in making predictions, understanding patterns and relationships in data, and drawing insights from observed data to inform decision-making and policy formulation.
          </div>
        </IonCardContent>
      </IonCard>

    </IonContent>
  );
};
  
export default EthereumLogarithmicRegression;