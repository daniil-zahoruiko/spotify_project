import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from 'react-router-dom';

import settings_en from "./translations/en/settings.json"
import settings_ua from "./translations/ua/settings.json"
import leftbar_en from "./translations/en/leftbar.json"
import leftbar_ua from "./translations/ua/leftbar.json"
import navbar_en from "./translations/en/navbar.json"
import navbar_ua from "./translations/ua/navbar.json"
import profile_en from "./translations/en/profile.json"
import profile_ua from "./translations/ua/profile.json"

import i18next from "i18next"
import {I18nextProvider} from "react-i18next"

i18next.init({
  interpolation:{escapeValue:true},
  lng:"en",
  resources:{
    en:{
      settings:settings_en,
      leftbar:leftbar_en,
      navbar:navbar_en,
      profile:profile_en
    },
    ua:{
      settings:settings_ua,
      leftbar:leftbar_ua,
      navbar:navbar_ua,
      profile:profile_ua
    }
  }
})

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <I18nextProvider i18n={i18next}>
        <App/>
      </I18nextProvider>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
