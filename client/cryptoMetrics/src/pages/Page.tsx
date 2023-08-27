import { IonButtons, IonContent, IonHeader, IonItem, IonMenuButton, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import { useParams } from 'react-router';
import './Page.css';
import cryptoMetricsLogo from '../assets/logo.svg';
import { pageComponents } from '../constants/PageComponents';

const Page: React.FC = () => {

  const { name } = useParams<{ name: string; }>();

  const page = pageComponents.find((page) => page.url === name);

  const pageTitle = page!.title;
  const PageComponent = page!.component;

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonButtons slot="start">
            <IonMenuButton />
          </IonButtons>
          <IonItem>
          <IonTitle size="small">{pageTitle}</IonTitle>
            <img src={cryptoMetricsLogo} alt="CryptoMetrics logo" slot="end" className='logo'/>
          </IonItem>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">{pageTitle}</IonTitle>
          </IonToolbar>
        </IonHeader>

        <IonContent>
          <PageComponent />
        </IonContent>
      </IonContent>
    </IonPage>
  );
};

export default Page;
