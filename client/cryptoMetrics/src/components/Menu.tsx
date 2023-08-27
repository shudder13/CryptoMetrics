import {
  IonAccordion,
  IonAccordionGroup,
  IonContent,
  IonIcon,
  IonItem,
  IonLabel,
  IonMenu,
  IonMenuToggle,
} from '@ionic/react';

import { useLocation } from 'react-router-dom';
import { appPages } from '../properties/MenuProperties';
import './Menu.css';


const Menu: React.FC = () => {
  const location = useLocation();

  return (
    <IonMenu contentId="main">
      <IonContent>
        <IonAccordionGroup multiple={true}>
          {appPages.map((appPage, index) => (
            <IonAccordion value={appPage.title} key={index}>
              <IonItem slot="header" color="light">
                {appPage.svgIcon 
                  ? <img src={appPage.svgIcon} alt={appPage.title} slot="start" className="logo" /> 
                  : <IonIcon aria-hidden="true" slot="start" ios={appPage.iosIcon} md={appPage.mdIcon} />
                }
                <IonLabel>{appPage.title}</IonLabel>
              </IonItem>
              <div slot="content">
                {appPage.subPages?.map((subPage, subIndex) => (
                  <IonMenuToggle key={subIndex} autoHide={false}>
                    <IonItem
                      className={location.pathname === subPage.url ? 'selected' : ''}
                      routerLink={subPage.url}
                      routerDirection="none"
                      lines="none"
                      detail={false}
                    >
                      <IonLabel className="submenu-label">{subPage.title}</IonLabel>
                    </IonItem>
                  </IonMenuToggle>
                ))}
              </div>
            </IonAccordion>
          ))}
        </IonAccordionGroup>
      </IonContent>
    </IonMenu>
  );
};

export default Menu;
