import { statsChartOutline, statsChartSharp, cashOutline, cashSharp, globeOutline, globeSharp, logoEuro, trendingUpOutline, trendingUpSharp } from "ionicons/icons";
import bitcoinLogo from '../assets/Bitcoin-logo.svg';
import ethereumLogo from '../assets/Ethereum-logo.svg';

interface SubPage {
  title: string;
  url: string;
}

interface AppPage {
  svgIcon?: string;
  iosIcon?: string;
  mdIcon?: string;
  title: string;
  subPages?: SubPage[];
}

const appPages: AppPage[] = [
    {
      title: 'Generic',
      iosIcon: statsChartOutline,
      mdIcon: statsChartSharp,
      subPages: [
        {
          title: 'Modern Portfolio Theory',
          url: '/page/modern-portfolio-theory',
        }
      ]
    },
    {
      title: 'Bitcoin',
      svgIcon: bitcoinLogo,
      subPages: [
        {
          title: 'Bitcoin Logarithmic Regression',
          url: '/page/Bitcoin-logarithmic-regression',
        },
        {
          title: 'Bitcoin Monthly Returns',
          url: '/page/Bitcoin-monthly-returns',
        },
        {
          title: 'Year-to-Date ROI',
          url: '/page/year-to-date-roi'
        },
        {
          title: 'Running 1 Year ROI',
          url: '/page/running-1-year-roi',
        },
        {
          title: 'Liveliness',
          url: '/page/liveliness',
        },
        {
          title: 'Addresses with balance ≥ 0.01',
          url: '/page/addresses-with-balance-gte-0-01',
        },
        {
          title: 'Addresses with balance ≥ 0.1',
          url: '/page/addresses-with-balance-gte-0-1',
        },
        {
          title: 'Addresses with balance ≥ 1',
          url: '/page/addresses-with-balance-gte-1',
        },
        {
          title: 'Addresses with balance ≥ 10',
          url: '/page/addresses-with-balance-gte-10',
        },
        {
          title: 'Addresses with balance ≥ 100',
          url: '/page/addresses-with-balance-gte-100',
        },
        {
          title: 'Addresses with balance ≥ 1k',
          url: '/page/addresses-with-balance-gte-1k',
        },
        {
          title: 'Addresses with balance ≥ 10k',
          url: '/page/addresses-with-balance-gte-10k',
        },
        {
          title: 'Addresses wave',
          url: '/page/addresses-wave',
        },
        {
          title: 'Number of whales',
          url: '/page/number-of-whales',
        },
        {
          title: 'Hodler net position change',
          url: '/page/hodler-net-position-change',
        },
        {
          title: 'Miner net position change',
          url: '/page/miner-net-position-change',
        },
        {
          title: 'Miner balance',
          url: '/page/miner-balance',
        },
        {
          title: 'Exchange netflow volume',
          url: '/page/exchange-netflow-volume',
        },
  
        // adrese cu balante peste 10k, 1k, 100, 10, 1, 0.1, 0.01 si eventual wave-ul acela, number of whales, hodler net position change
        // miner net position change, miner balance, exchange netflow volume, 
      ]
    },
    {
      title: 'Ethereum',
      svgIcon: ethereumLogo,
      iosIcon: cashOutline,
      mdIcon: cashSharp,
      subPages: [
        {
          title: 'Ethereum Logarithmic Regression',
          url: '/page/Ethereum-logarithmic-regression',
        },
        {
          title: 'Ethereum Monthly Returns',
          url: '/page/Ethereum-monthly-returns',
        },
      ]
    },
    {
      title: 'Macroeconomics',
      iosIcon: globeOutline,
      mdIcon: globeSharp,
      subPages: [
        {
          title: '',
          url: '',
        }
      ]
    },
    {
      title: 'Foreign exchange',
      iosIcon: logoEuro,
      mdIcon: logoEuro,
      subPages: [
        {
          title: '',
          url: '',
        }
      ]
    },
    {
      title: 'Stocks',
      iosIcon: trendingUpOutline,
      mdIcon: trendingUpSharp,
      subPages: [
        {
          title: '',
          url: '',
        }
      ]
    },
  ];

export { appPages };
export type { AppPage };
