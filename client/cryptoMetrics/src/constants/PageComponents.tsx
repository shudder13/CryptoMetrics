import BitcoinLogarithmicRegression from '../pages/Bitcoin/BitcoinLogarithmicRegression';
import BitcoinPiCycleTops from '../pages/Bitcoin/BitcoinPiCycleTops';
import EthereumLogarithmicRegression from '../pages/Ethereum/EthereumLogarithmicRegression';
import ModernPortfolioAnalysis from '../pages/Generic/ModernPortfolioTheory';

interface PageComponent {
    parent: string;
    title: string;
    url: string;
    component: React.FC;
}

export const pageComponents: PageComponent[] = [
    {
        parent: 'Generic',
        title: 'Modern Portfolio Analysis',
        url: 'modern-portfolio-analysis',
        component: ModernPortfolioAnalysis
    },
    {
        parent: 'Bitcoin',
        title: 'Bitcoin Logarithmic Regression',
        url: 'Bitcoin-logarithmic-regression',
        component: BitcoinLogarithmicRegression
    },
    {
        parent: 'Bitcoin',
        title: 'Bitcoin Pi Cycle tops',
        url: 'Bitcoin-pi-cycle-tops',
        component: BitcoinPiCycleTops
    },
    {
        parent: 'Ethereum',
        title: 'Ethereum Logarithmic Regression',
        url: 'Ethereum-logarithmic-regression',
        component: EthereumLogarithmicRegression
    }
];