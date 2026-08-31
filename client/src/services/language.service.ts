import { Injectable, signal } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { ApiConstants } from '../config';
import { HttpClient } from '@angular/common/http';
import { Culture } from '../interfaces';

@Injectable()
export class LanguageService {

  private readonly _language = new Subject<string>();
  private readonly _default_locale = 'cs';
  private readonly _locale = signal('cs');
  private readonly _supported_locales = ['cs', 'en'];
  private readonly _cultures = signal<Culture>(LanguageService.getCultures());
  private languageRequestId = 0;

  readonly localeSignal = this._locale.asReadonly();
  readonly culturesSignal = this._cultures.asReadonly();

  constructor(private http: HttpClient) { }

  get language(): Observable<string> {
    return this._language.asObservable();
  }

  get default_locale(): string {
    return this._default_locale;
  }

  get locale(): string {
    return this._locale();
  }

  get cultures(): Culture {
    return this._cultures();
  }

  private static getCultures(): Culture {
    // noinspection SpellCheckingInspection
    return {
      amount_description: 'Počet sklenic',
      certificates: 'Certifikáty',
      close: 'Zavřít',
      contact: 'Kontakt',
      czk: 'Kč',
      home: 'Domů',
      loading: 'Načítám',
      news: 'Novinky',
      not_in_store: 'Není skladem',
      photo: 'Foto',
      price_list: 'Ceník',
      prices_not_found: 'Ceníky nenalezeny',
      recipes: 'Recepty',
      region: 'Region',
      reservation_text: 'Pro rezervaci kontaktujte prosím Jana Šarocha na e-mailové adrese',
      reserve: 'Rezervovat',
      video: 'Video'
    }
  }

  setLanguage(locale: string) {
    if (this._supported_locales.indexOf(locale) >= 0) {
      this._locale.set(locale);
    }
    const requestedLocale = this.locale;
    const requestId = ++this.languageRequestId;
    const url = `${ ApiConstants.GET_CULTURES }?locale=${ requestedLocale }`;

    this.http.get<Culture>(url).subscribe(cultures => {
      if (requestId !== this.languageRequestId || requestedLocale !== this.locale) {
        return;
      }
      this._cultures.update(current => ({...current, ...cultures}));
      this._language.next(requestedLocale);
    });
  }
}
