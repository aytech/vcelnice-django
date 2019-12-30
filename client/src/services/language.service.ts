import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { ApiConstants } from '../config';
import { HttpClient } from '@angular/common/http';
import { Culture } from '../interfaces';

@Injectable()
export class LanguageService {

  constructor(private http: HttpClient) {
    this._cultures = LanguageService.getCultures();
  }

  get language(): Observable<string> {
    return this._language.asObservable();
  }

  get default_locale(): string {
    return this._default_locale;
  }

  get locale(): string {
    return this._locale;
  }

  get cultures(): Culture {
    return this._cultures;
  }

  private _language: Subject<string> = new Subject<string>();
  private _default_locale = 'cs';
  private _locale = 'cs';
  private _supported_locales = ['cs', 'en'];
  private _cultures: Culture;

  private static getCultures() {
    // noinspection SpellCheckingInspection
    return {
      amount_description: 'Počet sklenic',
      certificates: 'Certifikáty',
      close: 'Zavřít',
      contact: 'Kontakt',
      contact_form: 'Kontaktní formulář',
      czk: 'Kč',
      enter_email: 'Zadejte platnou e-mailovou adresu',
      enter_amount: 'Zadejte počet',
      error_empty_message: 'Prosím, zadejte svou zprávu',
      home: 'Domů',
      loading: 'Načítám',
      ok_message_sent: 'Zpráva byla odeslána, děkujeme',
      news: 'Novinky',
      not_in_store: 'Není skladem',
      photo: 'Foto',
      pickup_location: 'Vyzvednutí na adrese',
      price_list: 'Ceník',
      prices_not_found: 'Ceníky nenalezeny',
      recipes: 'Recepty',
      region: 'Region',
      reservation_ok: 'Rezervace byla úspěšně odeslána, děkuji',
      reserve: 'Rezervovat',
      send: 'Odeslat',
      server_error: 'Chyba serveru, zkuste to prosím později',
      video: 'Video',
      your_email: 'Vaše emailová adresa'
    };
  }

  setLanguage(locale: string) {
    if (this._supported_locales.indexOf(locale) >= 0) {
      this._locale = locale;
    }
    const url = `${ ApiConstants.GET_CULTURES }?locale=${ this._locale }`;
    this.http.get<Culture>(url).subscribe(cultures => {
      this._cultures = {...this.cultures, ...cultures};
      this._language.next(this._locale);
    });
  }
}
