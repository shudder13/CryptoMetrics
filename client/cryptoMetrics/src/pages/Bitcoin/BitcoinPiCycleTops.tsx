import { IonCard, IonCardContent, IonContent } from "@ionic/react";
import axios from "axios";
import Highcharts from 'highcharts';
import HighchartsReact from "highcharts-react-official";
import highContrastDark from 'highcharts/themes/high-contrast-dark';
import { useEffect, useState } from "react";
import { PiCycleTopsColor } from "../../constants/Constants";

highContrastDark(Highcharts);

const BitcoinPiCycleTops: React.FC = () => {
  const [priceData, setPriceData] = useState<any[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [piCycleTops, setPiCycleTops] = useState<any[]>([]);
  const [movingAveragesData, setMovingAveragesData] = useState<any>({
    daily_MA_111_days: {},
    daily_MA_350_days_doubled: {},
    tops: []
  });
  const [showPiCycleTops, setShowPiCycleTops] = useState<boolean>(false);

  useEffect(() => {
    axios.get("http://localhost:5000/api/price-history/crypto/BTC")
    .then(response => {
      setPriceData(response.data);
    })
    .catch(error => {
      console.error(error);
    })
  }, []);

  useEffect(() => {
    const convertedData = Object.entries(priceData).map(([date, value]) => {
      return [new Date(date).getTime(), value.close];
    });

    setChartData(convertedData);
  }, [priceData]);

  useEffect(() => {
    axios.get("http://localhost:5000/api/analysis/Bitcoin-pi-cycle-tops")
      .then(response => {
        setMovingAveragesData(response.data);
        setPiCycleTops(response.data.tops);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  const ma111Series = Object.entries(movingAveragesData.daily_MA_111_days).map(([date, value]) => {
    return [new Date(date).getTime(), value];
  });

  const ma350Series = Object.entries(movingAveragesData.daily_MA_350_days_doubled).map(([date, value]) => {
    return [new Date(date).getTime(), value];
  });

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
      plotLines: showPiCycleTops
        ? piCycleTops.map((date: string) => ({
          value: new Date(date).getTime(),
          color: PiCycleTopsColor,
          width: 1,
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
        name: 'Bitcoin price',
        lineWidth: 2.2
      },
      {
        type: 'line',
        data: ma111Series,
        name: 'Daily MA 111 days',
        color: '#FF0000',
        lineWidth: 1
      },
      {
        type: 'line',
        data: ma350Series,
        name: 'Daily MA 350 days doubled',
        color: '#00FF00',
        lineWidth: 1
      },
      {
        type: 'line',
        data: [],
        name: 'Pi Cycle tops (golden crosses)',
        color: PiCycleTopsColor,
        visible: showPiCycleTops
      }
    ],
    plotOptions: {
      series: {
        events: {
          legendItemClick: function(event) {
            if (this.name === 'Pi Cycle tops (golden crosses)') {
              setShowPiCycleTops(!showPiCycleTops);
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
              The "Pi Cycle" indicator predicts high-value periods in Bitcoin's market cycles, except the first one. Developed in April 2019, it employs two moving averages – the 111-day and 350-day multiplied by 2 – to identify potential price tops, signaled by the "golden cross" event. Its name is derived from the ratio of these moving averages' lengths.
          </div>
          <div>
              This indicator offers valuable insights when used in correlation with other metrics such as logarithmic regression and market cycles. While not independently definitive, it helps investors spot optimal selling opportunities during periods of substantial growth. If Bitcoin's price experiences a significant upswing, particularly within 2 years after halving, and a "golden cross" appears between the moving averages, it might signal an advantageous time to sell.
          </div>
          <div>
              The "Pi Cycle" indicator bridges technical analysis with real-world market behavior, aiding investors in their decision-making process. As an integral part of a comprehensive analysis toolkit, it contributes to a better understanding of Bitcoin's price dynamics.
          </div>
        </IonCardContent>
    </IonCard>
    </IonContent>
    );
  };
  
export default BitcoinPiCycleTops;
