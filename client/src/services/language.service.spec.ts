import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { ApiConstants } from '@config';
import { LanguageService } from './language.service';

describe('LanguageService', () => {
  let service: LanguageService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        LanguageService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });

    service = TestBed.inject(LanguageService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('exposes the default locale and cultures through readonly signals', () => {
    expect(service.localeSignal()).toBe('cs');
    expect(service.culturesSignal().home).toBe('Domů');
    expect(service.culturesSignal().contact).toBe('Kontakt');
  });

  it('updates locale and merged cultures signals after loading a supported language', () => {
    const initialCultures = service.culturesSignal();

    service.setLanguage('en');

    const request = httpTesting.expectOne({
      method: 'GET',
      url: `${ApiConstants.GET_CULTURES}?locale=en`
    });
    request.flush({
      home: 'Home',
      news: 'News'
    });

    expect(service.localeSignal()).toBe('en');
    expect(service.culturesSignal()).not.toBe(initialCultures);
    expect(service.culturesSignal().home).toBe('Home');
    expect(service.culturesSignal().news).toBe('News');
    expect(service.culturesSignal().contact).toBe('Kontakt');
  });

  it('ignores an older translation response after the locale changes again', () => {
    service.setLanguage('en');
    const englishRequest = httpTesting.expectOne(
      `${ApiConstants.GET_CULTURES}?locale=en`
    );

    service.setLanguage('cs');
    const czechRequest = httpTesting.expectOne(
      `${ApiConstants.GET_CULTURES}?locale=cs`
    );

    czechRequest.flush({home: 'Aktuální domů'});
    englishRequest.flush({home: 'Stale Home'});

    expect(service.localeSignal()).toBe('cs');
    expect(service.culturesSignal().home).toBe('Aktuální domů');
  });
});
