import BitcoinLogarithmicRegression from '../pages/Bitcoin/BitcoinLogarithmicRegression';
import BitcoinMonthlyReturns from '../pages/Bitcoin/BitcoinMonthlyReturns';
import BitcoinYTDROI from '../pages/Bitcoin/BitcoinYTDROI';
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
        title: 'Bitcoin Monthly Returns',
        url: 'Bitcoin-monthly-returns',
        component: BitcoinMonthlyReturns
    },
    {
        parent: 'Bitcoin',
        title: 'Bitcoin Year-To-Date ROI',
        url: 'Bitcoin-ytd-roi',
        component: BitcoinYTDROI
    },
    {
        parent: 'Ethereum',
        title: 'Ethereum Logarithmic Regression',
        url: 'Ethereum-logarithmic-regression',
        component: EthereumLogarithmicRegression
    }
];