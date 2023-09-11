import { statsChartOutline, statsChartSharp, cashOutline, cashSharp } from "ionicons/icons";
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
          title: 'Bitcoin Pi Cycle tops',
          url: '/page/Bitcoin-pi-cycle-tops'
        },
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
      ]
    },
  ];

export { appPages };
export type { AppPage };
