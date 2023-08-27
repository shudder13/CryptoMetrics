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
          title: 'Modern Portfolio Analysis', // TODO refactoring
          url: '/page/modern-portfolio-analysis',
        }
      ]
    },
    {
      title: 'Bitcoin',
      svgIcon: bitcoinLogo,
      subPages: [
        {
          title: 'Bitcoin logarithmic regression',
          url: '/page/Bitcoin-logarithmic-regression',
        },
        {
          title: 'Bitcoin monthly returns',
          url: '/page/Bitcoin-monthly-returns',
        },
        {
          title: 'Bitcoin Year-To-Date ROI',
          url: '/page/Bitcoin-ytd-roi'
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
          title: 'Ethereum logarithmic regression',
          url: '/page/Ethereum-logarithmic-regression',
        },
        {
          title: 'Ethereum monthly returns',
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
